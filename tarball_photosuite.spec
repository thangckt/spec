### Update 26May: use tarball instead of rpm release.

Name:           photosuite
Version:        0.9.21
Release:        1%{?dist}
Summary:        A desktop image editor faithfully replicating classic Adobe Photoshop

License:        MIT
URL:            https://github.com/eolix/photosuite
Source0:        %{url}/releases/download/v%{version}/photosuite-%{version}-linux-x86_64.tar.gz


%define debug_package %{nil}
%define __strip /bin/true

%description
A desktop image editor faithfully replicating classic Adobe Photoshop with 1:1 native PSD/PSB compatibility

%prep
%autosetup -n photosuite-%{version}-linux-x86_64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/photosuite
mkdir -p %{buildroot}%{_libexecdir}/photosuite
cp -rp * %{buildroot}%{_libexecdir}/photosuite/

### Create symlink for main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/photosuite/bin/photosuite %{buildroot}%{_bindir}/photosuite

### Install desktop file
install -Dpm644 %{_libexecdir}/photosuite/shares/applications/io.github.eolix.PhotoSuite.desktop %{buildroot}%{_datadir}/applications/photosuite.desktop

### Install icon
install -Dpm644 %{_libexecdir}/photosuite/shares/icons/hicolor/128x128/apps/io.github.eolix.PhotoSuite.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/io.github.eolix.PhotoSuite.png

%files
%{_bindir}/photosuite
%{_libexecdir}/photosuite/
%{_datadir}/applications/photosuite.desktop
%{_datadir}/icons/hicolor/128x128/apps/io.github.eolix.PhotoSuite.png

%changelog
%autochangelog
