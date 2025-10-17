### This app builds using `yarn`, but Copr does not have it, using `npm` instead

Name:           github-desktop-plus
Version:        3.5.3.2
Release:        1%{?dist}
Summary:        GitHub Desktop Plus

License:        MIT
URL:            https://github.com/pol-rivero/github-desktop-plus
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# Skip debug info for bundled Node code
%global debug_package %{nil}

# We install the packaged Electron app produced by electron-builder into /opt
%global install_dir /opt/%{name}

ExclusiveArch:  x86_64

BuildRequires:  git
BuildRequires:  nodejs >= 22
BuildRequires:  npm
BuildRequires:  yarnpkg
BuildRequires:  python3
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  chrpath
BuildRequires:  libsecret-devel

# Runtime deps that Electron apps commonly need (matches upstream/AUR)
Requires:       git
Requires:       gtk3
Requires:       libsecret
Requires:       libXss
Requires:       nspr
Requires:       nss
Requires:       unzip

%description
GitHub Desktop Plus is a graphical Git client for managing GitHub repositories easily.

%prep
%autosetup -n %{name}-%{version}

# Initialize a lightweight git repo so build tooling that expects git works
git init
git config user.email "rpm@localhost"
git config user.name "RPM Builder"
git add -A
git commit -m "rpm init"

# Initialize and fetch submodules (requires network; keep full history to match recorded SHAs)
git submodule update --init --recursive

# Remove ts-node postinstall (not needed for packaged builds)
for f in package.json app/package.json; do
  sed -i '/"postinstall"/d' $f
done


%build
# Work around nodejs/io_uring issue seen in CI and AUR notes
export UV_USE_IO_URING=0
export NODE_ENV=production
export CI=1
export HOME=$PWD

# Use xvfb-run to give Electron a DISPLAY during dependency install and build
xvfb-run -a yarn install --frozen-lockfile --ignore-scripts
xvfb-run -a yarn build:prod

%install
# Install the packaged app produced by electron-builder
install -d %{buildroot}%{install_dir}
cp -a dist/github-desktop-plus-linux-x64/* %{buildroot}%{install_dir}/

# CLI helper shipped by upstream; make a user-visible symlink
# (The script exists inside resources/app/static/github)
chmod +x %{buildroot}%{install_dir}/resources/app/static/github
install -d %{buildroot}%{_bindir}
ln -s %{install_dir}/resources/app/static/github %{buildroot}%{_bindir}/github-desktop-plus-cli

# Wrapper launcher
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
APPDIR="%{install_dir}"
# Use system Electron sandbox if available; fallback still works
export DESKTOP_DISABLE_TELEMETRY=1
exec "$APPDIR/github-desktop-plus" "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=GitHub Desktop+
GenericName=Git GUI Client
Exec=github-desktop-plus %U
Icon=github-desktop-plus
Type=Application
Terminal=false
Categories=Development;RevisionControl;
StartupWMClass=GitHub Desktop
EOF

# Icons from packaged resources (multiple sizes available)
install -d %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps
install -d %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -m0644 %{buildroot}%{install_dir}/resources/app/static/logos/1024x1024.png %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/%{name}.png || :
install -m0644 %{buildroot}%{install_dir}/resources/app/static/logos/512x512.png  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png  || :
install -m0644 %{buildroot}%{install_dir}/resources/app/static/logos/256x256.png  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png  || :

# Optional: strip any odd RPATHs if vendor git binaries exist (rare after electron-builder)
if [ -d "%{buildroot}%{install_dir}/resources/app/node_modules/dugite/git/libexec/git-core" ]; then
  find "%{buildroot}%{install_dir}/resources/app/node_modules/dugite/git/libexec/git-core" -type f -exec chrpath --delete '{}' + 2>/dev/null || :
fi

# License
install -Dpm0644 LICENSE.md %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.md || \
  install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE || :

%post
# Nudge icon cache (best effort, non-fatal)
touch --no-create %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor || :
fi

%files
%license %{_datadir}/licenses/%{name}/LICENSE*
%{_bindir}/%{name}
%{_bindir}/github-desktop-plus-cli
%{install_dir}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/1024x1024/apps/%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%changelog
%autochangelog