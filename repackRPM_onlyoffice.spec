Name:           onlyoffice
Version:        9.1.0
Release:        1%{?dist}
Summary:        OnlyOffice Desktop Editors

License:        GNU Affero Public License v3
URL:            https://github.com/ONLYOFFICE/DesktopEditors
Source0:        %{url}/releases/download/v%{version}/onlyoffice-desktopeditors.x86_64.rpm

ExclusiveArch:  x86_64

%description
This is rpm package for ONLYOFFICE Desktop Editors.

%prep
# Nothing to do

%build
### Disable the RPATH QA check
export QA_RPATHS=$((0x0001|0x0002))

# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}


%files
/opt/onlyoffice/**
%{_datadir}/applications/onlyoffice-desktopeditors.desktop
%{_datadir}/icons/hicolor/*/apps/onlyoffice-desktopeditors.png
%{_datadir}/doc/**
%{_datadir}/licenses/**
/usr/bin/desktopeditors
/usr/bin/onlyoffice-desktopeditors

%changelog
%autochangelog