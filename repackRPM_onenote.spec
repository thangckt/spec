Name:           onenote
Version:        2025.10.101
Release:        1%{?dist}
Summary:        P3X OneNote Linux

License:        MIT License
URL:            https://github.com/patrikx3/onenote
Source0:        %{url}/releases/download/v%{version}/p3x-onenote-%{version}.x86_64.rpm


ExclusiveArch:  x86_64

## No generate dependencies (should avoid using this)
# AutoReqProv: no

%description
This is a wrapper for Microsoft OneNote.

%prep
# Nothing to do

%build
# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
/opt/P3X-OneNote/**
%{_datadir}/applications/p3x-onenote.desktop
%{_datadir}/icons/hicolor/*/apps/p3x-onenote.png
/usr/lib/.build-id/*

%changelog
%autochangelog