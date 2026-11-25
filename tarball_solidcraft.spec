
Name:           solidcraft
Version:        0.39.0
Release:        1%{?dist}
Summary:        A desktop image editor faithfully replicating classic Adobe Photoshop

License:        MIT
URL:            https://github.com/tangency-labs/solidcraft
Source0:        %{url}/releases/download/v%{version}/solidcraft-%{version}-linux-x86_64.tar.gz


%define debug_package %{nil}
%define __strip /bin/true

%description
A desktop image editor faithfully replicating classic Adobe Photoshop with 1:1 native PSD/PSB compatibility

%prep
%autosetup -n solidcraft-%{version}-linux-x86_64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/solidcraft
mkdir -p %{buildroot}%{_libexecdir}/solidcraft
cp -rp * %{buildroot}%{_libexecdir}/solidcraft/

### Symlink to main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/solidcraft/bin/solidcraft %{buildroot}%{_bindir}/solidcraft

### Install desktop file
install -Dpm644 %{buildroot}%{_libexecdir}/solidcraft/share/applications/io.tangencylabs.solidcraft.desktop \
    %{buildroot}%{_datadir}/applications/solidcraft.desktop

### Install icon
for res in 16 24 32 48 64 128 256 512; do
    install -Dpm644 %{buildroot}%{_libexecdir}/solidcraft/share/icons/hicolor/${res}x${res}/apps/io.tangencylabs.solidcraft.png\
        %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/io.tangencylabs.solidcraft.png
done

%files
%{_bindir}/solidcraft
%{_libexecdir}/solidcraft/
%{_datadir}/applications/solidcraft.desktop
%{_datadir}/icons/hicolor/*/apps/io.tangencylabs.solidcraft.png

%changelog
%autochangelog
