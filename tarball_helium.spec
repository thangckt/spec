### https://copr-dist-git.fedorainfracloud.org/packages/v8v88v8v88/helium/helium.git/tree/
### https://github.com/itexpert120/helium-browser-copr/blob/main/helium.spec
### https://github.com/imputnet/helium-linux/blob/main/package/helium.desktop

### Note: Copr can access github url `archives/refs/tags`, but cannot access `releases/download` url if use `autosetup`, and raise 404 errors.

Name:           helium
Version:        0.6.3.1
Release:        1%{?dist}
Summary:        Helium Browser - Privacy-focused Chromium fork

License:        BSD 3-Clause license
URL:            https://github.com/imputnet/helium-linux
#ource0:        https://github.com/imputnet/helium-linux/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz
Source0:        https://github.com/imputnet/helium-linux/archive/refs/tags/0.6.3.1.tar.gz


BuildArch:      x86_64

Requires:       desktop-file-utils
Requires:       gtk3
Requires:       libX11
Requires:       libdrm
Requires:       mesa-libGL

# Disable debug package
%define debug_package %{nil}
%define __strip /bin/true

%description
Helium Browser - A fast, privacy-focused Chromium fork based on ungoogled-chromium.
Best privacy by default, unbiased ad-blocking, no bloat and no noise.

%prep
%setup -q -n helium-%{version}-x86_64_linux

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