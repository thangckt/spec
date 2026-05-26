Name:           rgitui
Version:        0.2.2
Release:        1%{?dist}
Summary:        A GPU-accelerated desktop Git client built with GPUI and Rust.

License:        MIT
URL:            https://github.com/noahbclarkson/rgitui
Source0:        %{url}/releases/download/v%{version}/rgitui-%{version}-x86_64-linux.tar.gz
Source1:        https://github.com/noahbclarkson/rgitui/blob/main/assets/icons/app-icon-512.png?raw=true


AutoReqProv: no

### Disable debug package
%global debug_package %{nil}

%description
rgitui (prebuilt binary). This spec repackages the upstream tarball for distribution via Copr.

%prep
%autosetup -n rgitui-%{version}-x86_64-linux

%build
# Nothing to build

%install
### Copy all extracted files to /usr/share/rgitui
mkdir -p %{buildroot}%{_datadir}/rgitui
cp -r * %{buildroot}%{_datadir}/rgitui/

### Symlink main executable to /usr/bin/rgitui
mkdir -p %{buildroot}%{_bindir}
cp rgitui %{buildroot}%{_datadir}/rgitui/
ln -sf %{_datadir}/rgitui/rgitui %{buildroot}%{_bindir}/rgitui

### Create desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/rgitui.desktop <<'EOF'
[Desktop Entry]
Name=rgitui
Exec=rgitui %U
Terminal=false
Type=Application
Icon=rgitui
StartupWMClass=rgitui
MimeType=x-scheme-handler/x-github-client;x-scheme-handler/x-github-desktop-auth;x-scheme-handler/x-github-desktop-dev-auth;
Categories=Development;
EOF

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
cp %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%files
%{_bindir}/rgitui
%{_datadir}/rgitui/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%changelog
%autochangelog
