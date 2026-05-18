### https://github.com/hkdb/aerion/blob/main/docs/BUILD.md
### https://github.com/hkdb/aerion/blob/main/build/linux/install.sh
### Revise by Gemini

Name:           aerion
Version:        0.2.3
Release:        1%{?dist}
Summary:        An Open Source Lightweight E-Mail Client

License:        Apache-2.0
URL:            https://github.com/hkdb/aerion
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  golang gcc-c++ make pkgconfig nodejs npm
BuildRequires:  webkit2gtk4.1-devel gtk3-devel

%description
Aerion is an open source, lightweight email client built for people who want a modern email experience without the bloat.

%prep
%autosetup -n %{name}-%{version}

%build
###Setup local Go path constraints to run the build cleanly inside the Copr container sandbox
export GO111MODULE=on
export GOPATH="%{_builddir}/go"
export PATH="$GOPATH/bin:$PATH"

### Install Wails framework locally as required by the build automation pipeline
go install github.com/wailsapp/wails/v2/cmd/wails@latest

### Buidl using the native Makefile target for Linux
%make_build build-linux

%install
### Set standard system environment variable prefixes for the Makefile installation engine
%make_install PREFIX=%{_prefix}

%files
%license LICENSE
%{_bindir}/aerion
%{_datadir}/applications/io.github.hkdb.Aerion.desktop
%{_datadir}/icons/hicolor/256x256/apps/io.github.hkdb.Aerion.png

%changelog
%autochangelog
