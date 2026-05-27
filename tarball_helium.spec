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

BuildRequires:  desktop-file-utils
Requires:       gtk3 libX11 libdrm mesa-libGL libglvnd-glx libglvnd-egl vulkan-loader mesa-dri-drivers

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
### Copy all extracted files to /usr/libexec/helium
mkdir -p %{buildroot}%{_libexecdir}/helium
cp -r * %{buildroot}%{_libexecdir}/helium/

### Wrapper script for main executable in /usr/bin/helium
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/helium << 'EOF'
#!/bin/bash
# 1. Pass down Wayland display environment variables so the browser can see your desktop
export XDG_RUNTIME_DIR="/run/user/$(id -u)"

# 2. Force hardware graphics flags, bypass blocks, and use EGL for Wayland
FLAGS="--disable-gpu-sandbox \
       --ignore-gpu-blocklist \
       --use-gl=egl \
       --enable-features=Vulkan,VulkanFromANGLE,DefaultANGLEVulkan \
       --enable-accelerated-video-decode"

exec /usr/libexec/helium/helium $FLAGS "$@"
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
%{_libexecdir}/helium/
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png

%post
%{_bindir}/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
