Name:           onenote
Version:        2025.10.101
Release:        1%{?dist}
Summary:        P3X OneNote Linux

License:        MIT License
URL:            https://github.com/patrikx3/onenote
Source0:        %{url}/releases/download/v%{version}/p3x-onenote-%{version}.x86_64.rpm

## No generate dependencies (should avoid using this)
# AutoReqProv: no
%global debug_package %{nil}
%global _build_id_links none

%description
This is a wrapper for Microsoft OneNote.

%prep
# Nothing to do

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
%dir /opt/P3X-OneNote
/opt/P3X-OneNote/*
%{_datadir}/applications/p3x-onenote.desktop
%{_datadir}/icons/hicolor/*/apps/p3x-onenote.png

%changelog
%autochangelog