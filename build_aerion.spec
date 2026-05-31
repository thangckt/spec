### https://github.com/hkdb/aerion/blob/main/docs/BUILD.md
### https://github.com/hkdb/aerion/blob/main/build/linux/install.sh
### Revise by Gemini
### Retired. Since Aerion does not support EWS.

Name:           aerion
Version:        0.2.5
Release:        1%{?dist}
Summary:        An Open Source Lightweight E-Mail Client

License:        Apache-2.0
URL:            https://github.com/hkdb/aerion
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  golang gcc-c++ make pkgconfig nodejs npm
BuildRequires:  webkit2gtk4.1-devel gtk3-devel

### Disable debug package
%global debug_package %{nil}

%description
Aerion is an open source, lightweight email client built for people who want a modern email experience without the bloat.

%prep
%autosetup -n %{name}-%{version}

%build
### Setup Go paths and install Wails safely inside Copr's build workspace
export GO111MODULE=on
export GOPATH="%{_builddir}/go"
export GOCACHE="%{_builddir}/go-cache"
export PATH="$GOPATH/bin:$PATH"

mkdir -p $GOPATH $GOCACHE
go install github.com/wailsapp/wails/v2/cmd/wails@latest

### Build based on the native Makefile target for Linux
# This generates the binary at 'build/bin/aerion' and assets under 'build/linux/'
%make_build build-linux

%install
### Create all target directories and copy the pre-built binary and desktop assets explicitly (No 'make' invoked here)
### Executable binary
install -Dpm 0755 build/bin/aerion %{buildroot}%{_bindir}/aerion

### Desktop entry
# Add the environment variable to disable DMABUF renderer
sed -i 's|^Exec=aerion|Exec=env WEBKIT_DISABLE_DMABUF_RENDERER=1 aerion|' build/linux/aerion.desktop
install -Dpm 0644 build/linux/aerion.desktop %{buildroot}%{_datadir}/applications/aerion.desktop

### Icon
sed -i 's|^Icon=io.github.hkdb.Aerion|Icon=aerion|' build/linux/aerion.desktop
install -Dpm 0644 build/linux/aerion.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/aerion.png

%files
%license LICENSE
%{_bindir}/aerion
%{_datadir}/applications/aerion.desktop
%{_datadir}/icons/hicolor/256x256/apps/aerion.png

%changelog
%autochangelog
