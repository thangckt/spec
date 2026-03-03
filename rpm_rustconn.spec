Name:           rustconn
Version:        0.9.6
Release:        1%{?dist}
Summary:        Manage remote connections easily.

License:        GPL-3.0
URL:            https://github.com/totoshko88/RustConn
Source0:        %{url}/releases/download/v%{version}/rustconn-%{version}-%{release}.x86_64.rpm

%global debug_package %{nil}
%global _build_id_links none

%description
This is rpm package for RustConn.

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
%{_bindir}/rustconn
%dir /opt/rustconn
/opt/rustconn/*
%{_datadir}/applications/rustconn.desktop
%{_datadir}/icons/hicolor/*/apps/rustconn.png
%{_datadir}/doc/**
%{_datadir}/licenses/**

%exclude /usr/lib/.build-id

%changelog
%autochangelog