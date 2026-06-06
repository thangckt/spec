### https://copr-dist-git.fedorainfracloud.org/packages/v8v88v8v88/helium/helium.git/tree/helium.spec?h=f43
### https://github.com/itexpert120/helium-browser-copr/blob/main/helium.spec
### https://github.com/imputnet/helium-linux/blob/main/package/helium.desktop

Name:           helium
Version:        0.12.5.1
Release:        1%{?dist}
Summary:        A fast, privacy-focused Chromium fork

License:        BSD-3-Clause
URL:            https://github.com/imputnet/helium-linux
Source0:        %{url}/releases/download/%{version}/helium-%{version}-x86_64_linux.tar.xz

BuildRequires:  desktop-file-utils
Requires:       nss libX11 vulkan-loader hicolor-icon-theme
Requires:       glibc>=2.34

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

### Create symlink for main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/helium/helium-wrapper %{buildroot}%{_bindir}/helium

### Create desktop file (available in the tarball)
install -Dpm644 helium.desktop %{buildroot}%{_datadir}/applications/helium.desktop

### Install icon
install -Dpm644 product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/helium.png

%files
%license %{_libexecdir}/helium/apparmor.cfg
%{_bindir}/helium
%{_libexecdir}/helium/
%{_datadir}/applications/helium.desktop
%{_datadir}/icons/hicolor/256x256/apps/helium.png

%post
%{_bindir}/update-desktop-database &> /dev/null || :

%changelog
%autochangelog
