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
### Disable the RPATH QA check (avoid using: chrpath, patchelf)
export QA_RPATHS=$((0x0001|0x0002|0x0004|0x0008|0x0010|0x0020))

rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
%{_bindir}/mailspring
%dir %{_datadir}/mailspring
%{_datadir}/mailspring/*
%{_datadir}/appdata/*
%{_datadir}/applications/Mailspring.desktop
%{_datadir}/icons/hicolor/*/apps/mailspring.png

%changelog
%autochangelog