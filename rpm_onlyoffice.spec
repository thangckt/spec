Name:           onlyoffice
Version:        9.2.1
Release:        1%{?dist}
Summary:        OnlyOffice Desktop Editors

License:        GNU Affero Public License v3
URL:            https://github.com/ONLYOFFICE/DesktopEditors
Source0:        %{url}/releases/download/v%{version}/onlyoffice-desktopeditors.x86_64.rpm

%global debug_package %{nil}
%global _build_id_links none

%description
This is rpm package for ONLYOFFICE Desktop Editors.

%prep
# Nothing to do

%build
# Nothing to build

%install
### Disable the RPATH QA check (avoid using: chrpath, patchelf)
export QA_RPATHS=$((0x0001|0x0002))

rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}


%files
%{_bindir}/desktopeditors
%{_bindir}/onlyoffice-desktopeditors
%dir /opt/onlyoffice
/opt/onlyoffice/*
%{_datadir}/applications/onlyoffice-desktopeditors.desktop
%{_datadir}/icons/hicolor/*/apps/onlyoffice-desktopeditors.png
%{_datadir}/doc/**
%{_datadir}/licenses/**

%exclude /usr/lib/.build-id

%changelog
%autochangelog