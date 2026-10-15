
Name:           turbo-reader
Version:        0.31.0
Release:        1%{?dist}
Summary:        A modern RSS reader

License:        MIT
URL:            https://github.com/t21dev/turbo-reader
Source0:        %{url}/releases/download/v%{version}/Turbo.Reader-%{version}-1.x86_64.rpm


%define debug_package %{nil}
%define __strip /bin/true

%description
A modern RSS reader that is actually fast and actually small.

%prep
# Nothing to build

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
%{_bindir}/turbo-reader
%{_datadir}/applications/Turbo Reader.desktop
%{_datadir}/icons/hicolor/*/apps/turbo-reader.png

%changelog
%autochangelog
