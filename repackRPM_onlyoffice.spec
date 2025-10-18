Name:           onlyoffice
Version:        8.1.0
Release:        1%{?dist}
Summary:        OnlyOffice Desktop Editors

License:        GNU Affero Public License v3
URL:            https://github.com/ONLYOFFICE/DesktopEditors
Source0:        %{url}/releases/download/v%{version}/onlyoffice-desktopeditors.x86_64.rpm

ExclusiveArch:  x86_64
BuildRequires:  chrpath

%description
This is rpm package for ONLYOFFICE Desktop Editors.

%prep
# Nothing to do

%build
# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

### Fix invalid RPATHs safely: replace /opt/qt/... with $ORIGIN
find %{buildroot}/opt/onlyoffice/desktopeditors -type f -exec file {} \; | \
    grep ELF | cut -d: -f1 | while read f; do
        # Read current RPATH
        RPATH=$(chrpath -l "$f" 2>/dev/null | awk '{print $2}')
        if echo "$RPATH" | grep -q '/opt/qt/5.9.9/gcc_64/lib'; then
            echo "Fixing RPATH in $f"
            chrpath -r '$ORIGIN' "$f" || true
        fi
    done

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