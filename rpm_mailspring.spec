Name:           mailspring
Version:        1.17.1
Release:        1%{?dist}
Summary:        Mailspring is a new version of Nylas Mail

License:        GNU
URL:            https://github.com/Foundry376/Mailspring
Source0:        %{url}/releases/download/%{version}/mailspring-%{version}-0.1.x86_64.rpm

# AutoReqProv: no
%global debug_package %{nil}
%global _build_id_links none

%description
Mailspring offers a modern, clean UI with fast search and multi-account support.

%prep
# Nothing to do

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
%dir /opt/Mailspring
/opt/Mailspring/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
%autochangelog