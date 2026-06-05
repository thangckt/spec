### Update 26May: use tarball instead of rpm release.

Name:           electerm
Version:        3.15.32
Release:        1%{?dist}
Summary:        Terminal and remote connection client

License:        MIT
URL:            https://github.com/electerm/electerm
Source0:        %{url}/releases/download/v%{version}/electerm-%{version}-linux-x64.tar.gz
Source1:        https://github.com/electerm/electerm-resource/blob/master/res/imgs/electerm-round-128x128.png?raw=true

### Disable debug package
%global debug_package %{nil}

AutoReqProv: no

%description
Electerm (prebuilt binary). This spec repackages the upstream tarball for distribution via Copr.

%prep
%autosetup -n electerm-%{version}-linux-x64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/electerm
mkdir -p %{buildroot}%{_libexecdir}/electerm
cp -r * %{buildroot}%{_libexecdir}/electerm/

### Wrapper script for main executable in /usr/bin/electerm
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/electerm << 'EOF'
#!/bin/bash
exec /usr/libexec/electerm/electerm "$@"
EOF
chmod +x %{buildroot}%{_bindir}/electerm

### Install desktop file
cat > electerm.desktop <<'EOF'
[Desktop Entry]
Name=electerm
Exec=electerm %U
Terminal=false
Type=Application
Icon=electerm
StartupWMClass=electerm
Comment=Terminal/ssh/telnet/serialport/sftp client(linux, mac, win)
MimeType=x-scheme-handler/ssh;x-scheme-handler/telnet;x-scheme-handler/rdp;x-scheme-handler/vnc;x-scheme-handler/serial;x-scheme-handler/spice;x-scheme-handler/electerm;
Categories=Development;System;TerminalEmulator;
EOF
install -Dpm644 electerm.desktop %{buildroot}%{_datadir}/applications/electerm.desktop

### Install icon
install -Dpm644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/electerm.png

%files
%{_bindir}/electerm
%{_libexecdir}/electerm/
%{_datadir}/applications/electerm.desktop
%{_datadir}/icons/hicolor/128x128/apps/electerm.png

%changelog
%autochangelog
