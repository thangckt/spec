
Name:           solidscraft
Version:        0.49.0
Release:        1%{?dist}
Summary:        A desktop image editor faithfully replicating classic Adobe Photoshop

License:        MIT
URL:            https://github.com/tangency-labs/solidscraft
Source0:        %{url}/releases/download/v%{version}/solidscraft-%{version}-linux-x86_64.tar.gz


%define debug_package %{nil}
%define __strip /bin/true

%description
A desktop image editor faithfully replicating classic Adobe Photoshop with 1:1 native PSD/PSB compatibility

%prep
%autosetup -n solidscraft-%{version}-linux-x86_64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/libexec/solidscraft
mkdir -p %{buildroot}%{_libexecdir}/solidscraft
cp -rp * %{buildroot}%{_libexecdir}/solidscraft/

### Symlink to main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/solidscraft/bin/solidscraft %{buildroot}%{_bindir}/solidscraft

### Install desktop file
install -Dpm644 %{buildroot}%{_libexecdir}/solidscraft/share/applications/io.tangencylabs.solidcraft.desktop \
    %{buildroot}%{_datadir}/applications/solidscraft.desktop

### Install icon
for res in 16 24 32 48 64 128 256 512; do
    install -Dpm644 %{buildroot}%{_libexecdir}/solidscraft/share/icons/hicolor/${res}x${res}/apps/io.tangencylabs.solidcraft.png\
        %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/io.tangencylabs.solidcraft.png
done

%files
%{_bindir}/solidscraft
%{_libexecdir}/solidscraft/
%{_datadir}/applications/solidscraft.desktop
%{_datadir}/icons/hicolor/*/apps/io.tangencylabs.solidcraft.png

%changelog
%autochangelog
