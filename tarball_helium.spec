### https://copr-dist-git.fedorainfracloud.org/packages/v8v88v8v88/helium/helium.git/tree/helium.spec?h=f43
### https://github.com/itexpert120/helium-browser-copr/blob/main/helium.spec
### https://github.com/imputnet/helium-linux/blob/main/package/helium.desktop

Name:           helium
Version:        0.12.4.1
Release:        1%{?dist}
Summary:        Helium Browser

License:        BSD 3-Clause
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz

Requires:       desktop-file-utils
Requires:       gtk3 libX11 libdrm mesa-libGL

### Disable debug package
%define debug_package %{nil}
%define __strip /bin/true

%description
Helium Browser - A fast, privacy-focused Chromium fork based on ungoogled-chromium.

%prep
%autosetup -n helium-%{version}-x86_64_linux

%build
# Nothing to build

%install
### Copy all extracted files to /usr/share/helium
mkdir -p %{buildroot}%{_datadir}/helium
cp -r * %{buildroot}%{_datadir}/helium/

# Find and link the main executable to /usr/bin/helium
# The executable might be named 'helium' or 'chrome' in the extracted files
mkdir -p %{buildroot}%{_bindir}
if [ -f chrome ]; then
    cp chrome %{buildroot}%{_datadir}/helium/
    ln -sf %{_datadir}/helium/chrome %{buildroot}%{_bindir}/helium
elif [ -f helium ]; then
    cp helium %{buildroot}%{_datadir}/helium/
    ln -sf %{_datadir}/helium/helium %{buildroot}%{_bindir}/helium
fi

### Create desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/helium.desktop <<'EOF'
[Desktop Entry]
Name=Helium Browser
Exec=helium %U
StartupWMClass=helium
Terminal=false
Icon=helium
Type=Application
Categories=Network;WebBrowser;

[Desktop Action new-window]
Name=New Window
Exec=helium

[Desktop Action new-private-window]
Name=New Incognito Window
Exec=helium --incognito
EOF

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
if [ -f product_logo_256.png ]; then
    cp product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png
else
    # Create a simple placeholder icon if logo not found
    touch %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png
fi

%files
%{_datadir}/helium/
%{_bindir}/helium
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png

%post
%{_bindir}/update-desktop-database &> /dev/null || :

%postun
%{_bindir}/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
