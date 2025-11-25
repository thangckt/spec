### ref: https://github.com/terrapkg/packages/blob/frawhide/anda/devs/zed/stable/zed.spec

Name:           zed
Version:        0.213.7
Release:        1%{?dist}
Summary:        High-performance, multiplayer code editor

License:        AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://github.com/zed-industries/zed
Source0:        %{url}/releases/download/%{version}/zed-linux-x86_64.tar.gz


BuildArch:      x86_64

Requires:       desktop-file-utils
Requires:       gtk3 libX11 libdrm mesa-libGL

# Disable debug package
%define debug_package %{nil}
%define __strip /bin/true

%description
Code at the speed of thought — Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.

%prep
%autosetup -n zed-%{version}-x86_64_linux

%build
# Nothing to build

%install
### Create directories
mkdir -p %{buildroot}/usr/share/zed
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps

### Copy all extracted files to /usr/share/zed
cp -r * %{buildroot}/usr/share/zed/

# Find and link the main executable
# The executable might be named 'zed' or 'chrome' in the extracted files
if [ -f chrome ]; then
    cp chrome %{buildroot}/usr/share/zed/
    ln -sf /usr/share/zed/chrome %{buildroot}/usr/bin/zed
elif [ -f zed ]; then
    cp zed %{buildroot}/usr/share/zed/
    ln -sf /usr/share/zed/zed %{buildroot}/usr/bin/zed
fi

### Create desktop entry
cat > %{buildroot}%{_datadir}/applications/zed.desktop <<'EOF'
[Desktop Entry]
[Desktop Entry]
Name=Zed Editor
GenericName=Text Editor
Exec=zed %U
Icon=zed
Type=Application
StartupNotify=true
Categories=Utility;TextEditor;Development;IDE;
MimeType=text/plain;application/x-zerosize;x-scheme-handler/zed;
Actions=NewWorkspace;
Keywords=zed;
StartupWMClass=dev.zed.Zed

[Desktop Action NewWorkspace]
Name=Open a new workspace
Exec=zed --new %U
EOF

### Use the product logo as icon
if [ -f product_logo_256.png ]; then
    cp product_logo_256.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/zed.png
else
    # Create a simple placeholder icon if logo not found
    touch %{buildroot}/usr/share/icons/hicolor/256x256/apps/zed.png
fi

%files
/usr/share/zed/
/usr/bin/zed
/usr/share/applications/zed.desktop
/usr/share/icons/hicolor/256x256/apps/zed.png

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
