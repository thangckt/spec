### DO NOT replace bundled git with system git. It will break the app.
### The bundled git is not pure git, it has customize with extra features.

Name:           github-desktop-plus
Version:        3.5.5.0
Release:        1%{?dist}
Summary:        GitHub Desktop Plus

License:        MIT
URL:            https://github.com/pol-rivero/github-desktop-plus
Source0:        %{url}/releases/download/v%{version}/GitHubDesktopPlus-v%{version}-linux-x86_64.rpm

Requires:       git-core

%description
GitHub Desktop Plus is a graphical Git client for managing GitHub repositories easily.
This spec repackages the upstream RPM for Copr and uses system Git.

%prep
# Nothing to build

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

### Remove bundled Git (built against libcurl-gnutls, incompatible with Fedora 43)
rm -rf %{buildroot}/usr/lib/%{name}/resources/app/git

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
/usr/lib/%{name}/**
/usr/share/doc/%{name}/copyright

%changelog
%autochangelog
