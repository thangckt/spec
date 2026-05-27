### https://copr-dist-git.fedorainfracloud.org/packages/v8v88v8v88/helium/helium.git/tree/helium.spec?h=f43
### https://github.com/itexpert120/helium-browser-copr/blob/main/helium.spec
### https://github.com/imputnet/helium-linux/blob/main/package/helium.desktop

Name:           helium
Version:        0.12.3.1
Release:        1%{?dist}
Summary:        Helium Browser

License:        BSD 3-Clause
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz

BuildRequires:  desktop-file-utils
### Added libglvnd-glx and vulkan-loader for modern WebGL/GPU acceleration support
Requires:       gtk3 libX11 libdrm mesa-libGL libglvnd-glx vulkan-loader

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

### Create a wrapper script instead of a symlink. This ensures Chromium knows its exact execution directory and preserves the sandbox/GPU environment
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/helium << 'EOF'
#!/bin/bash
exec /usr/share/helium/helium "$@"
EOF
chmod +x %{buildroot}%{_bindir}/helium

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
cp product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png

%files
%{_bindir}/helium
%{_datadir}/helium/
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png

%post
%{_bindir}/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
