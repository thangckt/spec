Name:           electerm
Version:        2.5.6
Release:        1%{?dist}
Summary:        Terminal and remote connection client

License:        MIT
URL:            https://github.com/electerm/electerm
Source0:        %{url}/releases/download/v%{version}/electerm-%{version}-linux-x86_64.rpm

AutoReqProv: no
%global debug_package %{nil}
%global _build_id_links none

%description
Electerm (prebuilt binary). This package simply repackages the upstream RPM for distribution via Copr.

%prep
# Nothing to do

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
%dir /opt/electerm
/opt/electerm/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude /usr/lib/.build-id

%changelog
%autochangelog
