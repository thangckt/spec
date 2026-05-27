### This package use system Git, unlike github-desktop which bundles its own Git.

Name:           servo
Version:        0.1.0
Release:        1%{?dist}
Summary:        Web browser engine written in the Rust language

License:        MIT
URL:            https://github.com/servo/servo
Source0:        %{url}/releases/download/v%{version}/servo-x86_64-linux-gnu.tar.gz

### Disable debug package
%global debug_package %{nil}

%description
servo (prebuilt binary). This spec repackages the upstream tarball for distribution via Copr.

%prep
%autosetup -n servo

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/servo
mkdir -p %{buildroot}%{_libexecdir}/servo
cp -r * %{buildroot}%{_libexecdir}/servo/

### Wrapper script for main executable in /usr/bin/servo
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/servo << 'EOF'
#!/bin/bash
exec /usr/libexec/servo/servoshell "$@"
EOF
chmod +x %{buildroot}%{_bindir}/servo

### Create desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/servo.desktop <<'EOF'
[Desktop Entry]
Name=Servo Web Browser
Exec=servo %u
Terminal=false
Icon=servo
Type=Application
MimeType=text/html;text/xml;application/xhtml+xml;text/mml;x-scheme-handler/http;x-scheme-handler/https;
Categories=Network;WebBrowser;
StartupWMClass=org.servo.Servo

[Desktop Action new-window]
Name=Open a New Window
Exec=servo %u
EOF

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp resources/servo_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%files
%{_bindir}/servo
%{_libexecdir}/servo/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%changelog
%autochangelog
