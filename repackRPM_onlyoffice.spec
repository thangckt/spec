Name:           onlyoffice
Version:        8.1.0
Release:        1%{?dist}
Summary:        OnlyOffice Desktop Editors

License:        GNU Affero Public License v3
URL:            https://github.com/ONLYOFFICE/DesktopEditors
Source0:        %{url}/releases/download/v%{version}/onlyoffice-desktopeditors.x86_64.rpm

ExclusiveArch:  x86_64
BuildRequires:  chrpath

## No generate dependencies (should avoid using this)
# AutoReqProv: no

%description
This is rpm package for ONLYOFFICE Desktop Editors.

%prep
# Nothing to do

%build
# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

### Strip invalid RPATHs from all ELF binaries (shared objects and executables)
find %{buildroot} -type f \( -name '*.so' -o -perm -111 \) -exec sh -c '
    for bin; do
        if file "$bin" | grep -q ELF && chrpath -l "$bin" 2>/dev/null | grep -q "/workspace/"; then
            chrpath -d "$bin"
        fi
    done
' sh {} +

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