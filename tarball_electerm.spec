### Update 26May: use tarball instead of rpm release.

Name:           electerm
Version:        3.9.15
Release:        1%{?dist}
Summary:        Terminal and remote connection client

License:        MIT
URL:            https://github.com/electerm/electerm
Source0:        %{url}/releases/download/v%{version}/electerm-%{version}-linux-x64.tar.gz

### Disable debug package
%global debug_package %{nil}

%description
Electerm (prebuilt binary). This spec repackages the upstream tarball for distribution via Copr.

%prep
%autosetup -n electerm-%{version}-linux-x64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/share/electerm
mkdir -p %{buildroot}%{_datadir}/electerm
cp -r * %{buildroot}%{_datadir}/electerm/

### Symlink main executable to /usr/bin/electerm
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_datadir}/electerm/bin/electerm %{buildroot}%{_bindir}/electerm

### Create desktop entry
cat > %{buildroot}%{_datadir}/applications/electerm.desktop <<'EOF'
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

%files
%{_bindir}/electerm
%{_datadir}/electerm
%{_datadir}/applications/%{name}.desktop


%changelog
%autochangelog
