### This package use system Git, unlike github-desktop which bundles its own Git.

Name:           rgitui
Version:        0.2.2
Release:        1%{?dist}
Summary:        A GPU-accelerated desktop Git client built with GPUI and Rust.

License:        MIT
URL:            https://github.com/noahbclarkson/rgitui
Source0:        %{url}/releases/download/v%{version}/rgitui-%{version}-x86_64-linux.tar.gz
Source1:        https://github.com/noahbclarkson/rgitui/blob/main/assets/icons/app-icon-256.png?raw=true

Requires:       git

### Disable debug package
%global debug_package %{nil}

%description
rgitui (prebuilt binary). This spec repackages the upstream tarball for distribution via Copr.

%prep
%autosetup -n rgitui

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/rgitui
mkdir -p %{buildroot}%{_libexecdir}/rgitui
cp -r * %{buildroot}%{_libexecdir}/rgitui/

### Wrapper script for main executable in /usr/bin/rgitui
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/rgitui << 'EOF'
#!/bin/bash
exec /usr/libexec/rgitui/rgitui "$@"
EOF
chmod +x %{buildroot}%{_bindir}/rgitui

### Create desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/rgitui.desktop <<'EOF'
[Desktop Entry]
Name=Rust GitUI
Comment=A GPU-accelerated desktop Git client built with GPUI and Rust.
Exec=rgitui %U
Terminal=false
Type=Application
Icon=rgitui
StartupWMClass=rgitui
MimeType=x-scheme-handler/x-github-client;x-scheme-handler/x-github-desktop-auth;x-scheme-handler/x-github-desktop-dev-auth;
Categories=Development;
EOF

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%files
%{_bindir}/rgitui
%{_datadir}/rgitui/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%changelog
%autochangelog
