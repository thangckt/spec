
Name:           photosplice
Version:        0.9.23
Release:        1%{?dist}
Summary:        A desktop image editor faithfully replicating classic Adobe Photoshop

License:        MIT
URL:            https://github.com/eolix/PhotoSplice
Source0:        %{url}/releases/download/v%{version}/photosplice-%{version}-linux-x86_64.tar.gz


%define debug_package %{nil}
%define __strip /bin/true

%description
A desktop image editor faithfully replicating classic Adobe Photoshop with 1:1 native PSD/PSB compatibility

%prep
%autosetup -n photosplice-%{version}-linux-x86_64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/photosplice
mkdir -p %{buildroot}%{_libexecdir}/photosplice
cp -rp * %{buildroot}%{_libexecdir}/photosplice/

### Symlink to main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/photosplice/bin/photosplice %{buildroot}%{_bindir}/photosplice

### Install desktop file
install -Dpm644 %{buildroot}%{_libexecdir}/photosplice/share/applications/io.github.eolix.PhotoSplice.desktop \
    %{buildroot}%{_datadir}/applications/photosplice.desktop

### Install icon
for res in 16 24 32 48 64 128 256; do
    install -Dpm644 %{buildroot}%{_libexecdir}/photosplice/share/icons/hicolor/${res}x${res}/apps/io.github.eolix.PhotoSplice.png \
        %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/io.github.eolix.PhotoSplice.png
done

%files
%{_bindir}/photosplice
%{_libexecdir}/photosplice/
%{_datadir}/applications/photosplice.desktop
%{_datadir}/icons/hicolor/*/apps/io.github.eolix.PhotoSplice.png

%changelog
%autochangelog
