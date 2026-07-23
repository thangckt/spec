### https://copr-dist-git.fedorainfracloud.org/packages/v8v88v8v88/helium/helium.git/tree/helium.spec?h=f43
### https://github.com/itexpert120/helium-browser-copr/blob/main/helium.spec
### https://github.com/imputnet/helium-linux/blob/main/package/helium.desktop

Name:           helium
Version:        0.14.8.2
Release:        1%{?dist}
Summary:        A fast, privacy-focused Chromium fork

License:        BSD-3-Clause
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz

BuildRequires:  desktop-file-utils libglibutil-devel
Requires:       vulkan-loader

# Disable debuginfo packaging and stripping for pre-compiled binaries
%global debug_package %{nil}
%global __strip /bin/true

%description
Helium Browser is a fast, privacy-focused Chromium fork based on ungoogled-chromium.

%prep
%autosetup -n helium-%{version}-x86_64_linux

%build
# Pre-compiled binary distribution.

%install
### Copy all extracted files to /usr/libexec/helium
mkdir -p %{buildroot}%{_libexecdir}/helium
cp -rp * %{buildroot}%{_libexecdir}/helium/

### Create symlink for main executable (wrapper existed)
# mkdir -p %{buildroot}%{_bindir}
# ln -sf %{_libexecdir}/helium/helium-wrapper %{buildroot}%{_bindir}/helium
# ln -sf %{_libexecdir}/helium/helium %{buildroot}%{_bindir}/helium

### Create wrapper script for main executable (to easy set execution flags)
cat > helium_wrapper << 'EOF'
#!/bin/bash
# FLAGS="--use-gl=angle --use-angle=swiftshader"
# exec %{_libexecdir}/helium/helium $FLAGS "$@"
exec %{_libexecdir}/helium/helium "$@"
EOF
install -Dpm755 helium_wrapper %{buildroot}%{_bindir}/helium

### Create desktop file (replace the existing one in the tarball)
cat > helium.desktop <<'EOF'
[Desktop Entry]
Name=Helium Web Browser
GenericName=Web Browser
Exec=helium %U
StartupWMClass=helium
Terminal=false
Icon=helium
Type=Application
Categories=Network;WebBrowser;
MimeType=application/pdf;application/rdf+xml;application/rss+xml;application/xhtml+xml;application/xhtml_xml;application/xml;image/gif;image/jpeg;image/png;image/webp;text/html;text/xml;x-scheme-handler/http;x-scheme-handler/https;
Actions=new-window;new-private-window;

[Desktop Action new-window]
Name=New Window
Exec=helium

[Desktop Action new-private-window]
Name=New Incognito Window
Exec=helium --incognito
EOF

desktop-file-validate helium.desktop
install -Dpm644 helium.desktop %{buildroot}%{_datadir}/applications/helium.desktop

### Copy icon
install -Dpm644 product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png

%files
%{_bindir}/helium
%{_libexecdir}/helium/
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png

%post
%{_bindir}/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
