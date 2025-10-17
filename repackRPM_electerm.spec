Name:           electerm
Version:        2.3.20
Release:        1%{?dist}
Summary:        terminal/ssh/telnet/serialport/RDP/VNC/sftp/ftp client

License:        MIT License
URL:            https://github.com/electerm/electerm
Source0:        %{url}/releases/download/v%{version}/electerm-%{version}-linux-x86_64.rpm

ExclusiveArch:  x86_64

## No generate dependencies (should avoid using this)
AutoReqProv: no

%description
RuskDesk (prebuilt binary). This package simply repackages the RPM for distribution via Copr.

%prep
# Nothing to do

%build
# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%files
/opt/electerm/**
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
/usr/lib/.build-id/*

%changelog
%autochangelog