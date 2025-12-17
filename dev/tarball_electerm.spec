### Use `tarball` instead of `RPM`

Name:           electerm
Version:        2.3.136
Release:        1%{?dist}
Summary:        Terminal and remote connection client

License:        MIT
URL:            https://github.com/electerm/electerm
Source0:        %{url}/releases/download/v%{version}/electerm-%{version}-linux-x64.tar.gz

%global debug_package %{nil}

%description
Electerm (prebuilt binary).

%prep
%autosetup -n electerm-%{version}-linux-x64

%build
# Nothing to build

%install
### Install the whole bundle under /usr/libexec/electerm
mkdir -p %{buildroot}%{_libexecdir}/electerm
cp -r * %{buildroot}%{_libexecdir}/electerm/

### Symlink main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/electerm/electerm %{buildroot}%{_bindir}/electerm

%files



%changelog
%autochangelog
