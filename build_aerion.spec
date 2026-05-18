### https://github.com/hkdb/aerion/blob/main/docs/BUILD.md
### https://github.com/hkdb/aerion/blob/main/build/linux/install.sh

Name:           aerion
Version:        0.2.3
Release:        1%{?dist}
Summary:        An Open Source Lightweight E-Mail Client

License:        Apache-2.0
URL:            https://github.com/hkdb/aerion
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  golang gcc-c++ pkgconfig nodejs npm
BuildRequires:  webkit2gtk4.1-devel gtk3-devel

%description
Aerion is an open source, lightweight email client built for people who want a modern email experience without the bloat.

%prep
%autosetup -n %{name}-%{version}

%build
### 1. Install the explicit version of the Wails CLI locally to build the project
export GO111MODULE=on
export GOPATH="%{_builddir}/go"
export PATH="$GOPATH/bin:$PATH"
go install github.com/wailsapp/wails/v2/cmd/wails@latest

### 2. Build the production asset pipeline (Wails automates frontend npm build & cgo compilation)
# Note: Aerion requires the webkit2_41 build tag for modern WebKit libraries on modern Fedora
wails build -tags

%install
### Install the compiled binary
mkdir -p %{buildroot}%{_bindir}
cp build/bin/aerion %{buildroot}%{_bindir}/aerion

### Desktop Entry
mkdir -p %{buildroot}%{_datadir}/applications
cp %{SOURCE1}/build/linux/aerion.desktop %{buildroot}%{_datadir}/applications/aerion.desktop

### Copy icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp %{SOURCE1}/build/linux/aerion.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/aerion.png

%files
%{_bindir}/aerion
%{_datadir}/aerion
%{_datadir}/applications/aerion.desktop
%{_datadir}/icons/hicolor/256x256/apps/aerion.png

%changelog
%autochangelog
