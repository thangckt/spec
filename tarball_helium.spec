### https://copr-dist-git.fedorainfracloud.org/packages/v8v88v8v88/helium/helium.git/tree/helium.spec?h=f43
### https://github.com/itexpert120/helium-browser-copr/blob/main/helium.spec
### https://github.com/imputnet/helium-linux/blob/main/package/helium.desktop

Name:           helium
Version:        0.10.5.1
Release:        1%{?dist}
Summary:        Helium Browser

License:        BSD 3-Clause
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz

Requires:       desktop-file-utils
Requires:       gtk3 libX11 libdrm mesa-libGL

# Disable debug package
%define debug_package %{nil}
%define __strip /bin/true

%description
Helium Browser - A fast, privacy-focused Chromium fork based on ungoogled-chromium.

%prep
%autosetup -n helium-%{version}-x86_64_linux

%build
# Nothing to build

%install
### Create directories
mkdir -p %{buildroot}/usr/share/helium
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps

### Copy all extracted files to /usr/share/helium
cp -r * %{buildroot}/usr/share/helium/

# Find and link the main executable
# The executable might be named 'helium' or 'chrome' in the extracted files
if [ -f chrome ]; then
    cp chrome %{buildroot}/usr/share/helium/
    ln -sf /usr/share/helium/chrome %{buildroot}/usr/bin/helium
elif [ -f helium ]; then
    cp helium %{buildroot}/usr/share/helium/
    ln -sf /usr/share/helium/helium %{buildroot}/usr/bin/helium
fi

### Create desktop entry
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

### Use the product logo as icon
if [ -f product_logo_256.png ]; then
    cp product_logo_256.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/helium.png
else
    # Create a simple placeholder icon if logo not found
    touch %{buildroot}/usr/share/icons/hicolor/256x256/apps/helium.png
fi

%files
/usr/share/helium/
/usr/bin/helium
/usr/share/applications/helium.desktop
/usr/share/icons/hicolor/256x256/apps/helium.png

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
