### https://github.com/hkdb/aerion/blob/main/docs/BUILD.md
### https://github.com/hkdb/aerion/blob/main/build/linux/install.sh

Name:           aerion
Version:        0.2.3
Release:        1%{?dist}
Summary:        An Open Source Lightweight E-Mail Client

License:        Apache-2.0
URL:            https://github.com/hkdb/aerion
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  go make pkgconfig

%description
Aerion is an open source, lightweight email client built for people who want a modern email experience without the bloat.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

### Desktop Entry
mkdir -p %{buildroot}%{_datadir}/applications
cp %{SOURCE1}/build/linux/aerion.desktop %{buildroot}%{_datadir}/applications/aerion.desktop

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp %{SOURCE1}/build/linux/aerion.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/aerion.png


%files
%{_bindir}/aerion
%{_datadir}/aerion
%{_datadir}/applications/aerion.desktop
%{_datadir}/icons/hicolor/256x256/apps/aerion.png

%changelog
%autochangelog
