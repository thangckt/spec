### Update 26May: use tarball instead of rpm release.

Name:           electerm
Version:        3.9.15
Release:        1%{?dist}
Summary:        Terminal and remote connection client

License:        MIT
URL:            https://github.com/electerm/electerm
Source0:        %{url}/releases/download/v%{version}/electerm-%{version}-linux-x64.tar.gz

### Disable debug package
%global debug_package %{nil}

%description
Electerm (prebuilt binary). This spec repackages the upstream tarball for distribution via Copr.

%prep
%autosetup -n electerm-%{version}-linux-x64

%build
# Nothing to build

%install
### Copy all extracted files to /usr/share/electerm
mkdir -p %{_datadir}/electerm
cp -r * %{_datadir}/electerm/

### Symlink main executable to /usr/bin/electerm
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_datadir}/electerm/bin/electerm %{buildroot}%{_bindir}/electerm

%files
%{_bindir}/electerm
%{_datadir}/electerm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
%autochangelog
