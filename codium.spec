### REF: https://gitlab.com/athenaos/packages/applications/vscodium/-/blob/main/rpm/vscodium.spec?ref_type=heads
### https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo
# This spec replaces `rustup` with `rust+cargo`

Name:           codium
Version:        1.104.16282
Release:        1%{?dist}
Summary:        Free/Libre Open Source Software Binaries of VSCode

License:        MIT
URL:            https://github.com/VSCodium/vscodium
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

ExclusiveArch:  x86_64
%global vscode_arch x64
%global debug_package %{nil}

BuildRequires:  gcc gcc-c++ make pkgconf git jq fakeroot ripgrep
BuildRequires:  python3 nodejs npm rust cargo
BuildRequires:  libX11-devel libxkbfile-devel libsecret-devel krb5-devel
Requires:       libX11 libxkbfile libsecret krb5-libs libstdc++ ripgrep

%description
VSCodium is a community-driven, freely-licensed binary distribution of Microsoft's VS Code.

%prep
%autosetup -n vscodium-%{version}
sed -i '/rustup /d' build_cli.sh

%build
# Environment setup
export VSCODE_ARCH=%{vscode_arch}
export VSCODE_QUALITY="stable"
export RELEASE_VERSION="%{version}"
export SHOULD_BUILD=yes
export SHOULD_BUILD_REH=no
export CI_BUILD=no
export OS_NAME=linux
export DISABLE_UPDATE=yes

# Build
./get_repo.sh
./build.sh

%install
mkdir -p %{buildroot}/usr/share/vscodium
cp -r VSCode-linux-*/* %{buildroot}/usr/share/vscodium/

# Symlink binary
mkdir -p %{buildroot}%{_bindir}
ln -s /usr/share/vscodium/bin/codium %{buildroot}%{_bindir}/codium

# Replace bundled ripgrep with system binary
ln -sf /usr/bin/rg %{buildroot}/usr/share/vscodium/resources/app/node_modules/@vscode/ripgrep/bin/rg

# Desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=VSCodium
GenericName=Text Editor
Exec=/usr/bin/codium %F
Icon=%{name}
Type=Application
StartupNotify=true
Categories=Utility;Development;IDE;
MimeType=text/plain;inode/directory;application/x-code-workspace;
Actions=new-empty-window;
Keywords=vscode;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=/usr/bin/codium --new-window %F
Icon=%{name}
EOF

# Icon
install -D -m644 VSCode-linux-%{vscode_arch}/resources/app/resources/linux/code.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# Strip native binaries
find %{buildroot}/usr/share/vscodium -type f -executable -exec strip --strip-unneeded '{}' + 2>/dev/null || :

# Remove duplicate native modules to avoid build-id collisions
# find %{buildroot}/usr/share/vscodium -type f -path "*/obj.target/*" -name "*.node" -delete

%files
%license LICENSE
%doc README.md
%{_bindir}/codium
%{_datadir}/vscodium
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

%changelog
%autochangelog
