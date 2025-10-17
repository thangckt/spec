Name:           onlyoffice
Version:        9.1.0
Release:        1%{?dist}
Summary:        OnlyOffice Desktop Editors

License:        GNU Affero Public License v3
URL:            https://github.com/ONLYOFFICE/DesktopEditors
Source0:        %{url}/releases/download/v%{version}/onlyoffice-desktopeditors.x86_64.rpm

ExclusiveArch:  x86_64
BuildRequires:  patchelf

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

### Fix RPATHs to be relative (inside same dir)
find %{buildroot}/opt/onlyoffice -type f -exec file {} \; | \
  grep ELF | cut -d: -f1 | while read f; do
    patchelf --set-rpath '$ORIGIN:$ORIGIN/..:$ORIGIN/../lib' "$f" 2>/dev/null || true
done

### Create wrapper script for OnlyOffice
mkdir -p %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/onlyoffice-desktopeditors << 'EOF'
#!/bin/bash
APPDIR="/opt/onlyoffice/desktopeditors"
export LD_LIBRARY_PATH="$APPDIR:$APPDIR/lib:$LD_LIBRARY_PATH"
exec "$APPDIR/DesktopEditors" "$@"
EOF
chmod +x %{buildroot}%{_bindir}/onlyoffice-desktopeditors

cat > %{buildroot}%{_bindir}/desktopeditors << 'EOF'
#!/bin/bash
exec /usr/bin/onlyoffice-desktopeditors "$@"
EOF
chmod +x %{buildroot}%{_bindir}/desktopeditors

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