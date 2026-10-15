
Name:           flectar-mail
Version:        0.1.0-alpha.7
Release:        1%{?dist}
Summary:        A modern RSS reader

License:        GNU-v3
URL:            https://github.com/flectar/mail
Source0:        %{url}/releases/download/v%{version}/flectar-mail-%{version}-linux-x64.rpm


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

### rename
# mv "%{buildroot}%{_datadir}/applications/Turbo Reader.desktop" "%{buildroot}%{_datadir}/applications/flectar-mail.desktop"

%files
%{_bindir}/flectar-mail
%{_datadir}/applications/flectar-mail.desktop
%{_datadir}/icons/hicolor/*/apps/flectar-mail.png

%changelog
%autochangelog
