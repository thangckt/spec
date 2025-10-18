Name:           onlyoffice
Version:        9.1.0
Release:        1%{?dist}
Summary:        OnlyOffice Desktop Editors

License:        GNU Affero Public License v3
URL:            https://github.com/ONLYOFFICE/DesktopEditors
Source0:        %{url}/releases/download/v%{version}/onlyoffice-desktopeditors.x86_64.rpm

ExclusiveArch:  x86_64
BuildRequires:  chrpath patchelf

%description
This is rpm package for ONLYOFFICE Desktop Editors.

%prep
# Nothing to do

%build
# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

### Set RUNPATH on every ELF so the loader finds the bundled libs
find %{buildroot}/opt/onlyoffice/desktopeditors -type f -exec file {} \; | \
    grep ELF | cut -d: -f1 | while read -r f; do
        # Put the binary's dir, its parent and ../lib in the runpath
        patchelf --set-rpath '$ORIGIN:$ORIGIN/..:$ORIGIN/../lib' "$f" || {
            echo "patchelf failed for $f, trying chrpath fallback"
            chrpath -r '$ORIGIN:$ORIGIN/..:$ORIGIN/../lib' "$f" || true
        }
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