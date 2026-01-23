### REF: https://www.zotero.org/support/dev/client_coding/building_the_desktop_app
### building Zotero from source (dependences: nodejs, npm) is quite complex and may still have issues -> Use the official binary (Recommended)
### Note on changing download URL in Zotero 8:
# Zetero 7: https://download.zotero.org/client/release/7.0.32/Zotero-7.0.32_linux-x86_64.tar.bz2
# Zotero 8: https://download.zotero.org/client/release/8.0/Zotero-8.0_linux-x86_64.tar.xz

Name:           zotero
Version:        8.0
Release:        1%{?dist}
Summary:        Zotero Reference Manager

License:        AGPL-3.0-only
URL:            https://www.zotero.org/
Source0:        https://download.zotero.org/client/release/%{version}/Zotero-%{version}_linux-x86_64.tar.xz

Requires:       gtk3 libXt libX11 dbus-glib

%global debug_package %{nil}
%global _build_id_links none

%description
Zotero is a free, easy-to-use tool to help you collect, organize, cite, and share research. This package contains the official Zotero binary.

%prep
%setup -q -n Zotero_linux-x86_64

%build
# Nothing to build - this is a binary package

%install
### Install whole zotero package under /opt/zotero
mkdir -p %{buildroot}/opt/zotero
cp -a * %{buildroot}/opt/zotero/

### Create wrapper script
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/zotero << 'EOF'
#!/bin/bash
export LD_LIBRARY_PATH=/opt/zotero:$LD_LIBRARY_PATH
exec /opt/zotero/zotero "$@"
EOF
chmod +x %{buildroot}%{_bindir}/zotero

### Create desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=Zotero
Comment=Zotero Reference Manager
Exec=zotero
Icon=zotero
Type=Application
Categories=Office;Education;Science;
EOF

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
cp icons/icon128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/zotero.png

%files
%dir /opt/zotero
/opt/zotero/*
%{_bindir}/zotero
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/zotero.png

%changelog
%autochangelog