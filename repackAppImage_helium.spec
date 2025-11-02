### Repack Helium AppImage into an RPM

Name:           helium
Version:        0.5.8.1
Release:        1%{?dist}
Summary:        Helium Browser

License:        BSD 3-Clause license
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}.x86_64.AppImage


ExclusiveArch:  x86_64
BuildRequires:  desktop-file-utils

## No generate dependencies (should avoid using this)
# AutoReqProv: no

%description
Helium is a new browser.

%prep
# Nothing to do

%build
# Nothing to build

%install
### Extract AppImage
chmod +x %{SOURCE0}
%{SOURCE0} --appimage-extract

### Copy extracted binaries and resources
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

cp -a squashfs-root/usr/* %{buildroot}/usr/ || true

# # If the app doesn’t install to /usr, copy main binary manually
# if [ ! -f %{buildroot}/usr/bin/helium ]; then
#     install -m 0755 squashfs-root/AppRun %{buildroot}/usr/bin/helium
# fi

# # Install icon (if exists)
# if [ -f squashfs-root/helium.png ]; then
#     install -m 0644 squashfs-root/helium.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png
# fi

### Create desktop entry
cat > %{buildroot}%{_datadir}/applications/helium.desktop <<'EOF'
[Desktop Entry]
Name=Helium
GenericName=Web Browser
Exec=chromium %U
StartupNotify=true
StartupWMClass=helium
Terminal=false
Icon=helium
Type=Application
Categories=Network;WebBrowser;
EOF


%files
%license squashfs-root/usr/share/licenses/* || :
%doc squashfs-root/usr/share/doc/* || :
%{_bindir}/helium
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/*/apps/helium.png

%changelog
%autochangelog