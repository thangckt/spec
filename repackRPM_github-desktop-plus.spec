### DO NOT replace bundled git with system git. It will break the app.
### The bundled git is not pure git, it has customize with extra features.

Name:           github-desktop-plus
Version:        3.5.3.10
Release:        1%{?dist}
Summary:        GitHub Desktop Plus

License:        MIT
URL:            https://github.com/pol-rivero/github-desktop-plus
Source0:        %{url}/releases/download/v%{version}/GitHubDesktopPlus-v%{version}-linux-x86_64.rpm

ExclusiveArch:  x86_64
BuildRequires:  chrpath, patchelf

## Filter out the problematic dependency: `libcurl-gnutls`
%global __requires_exclude ^libcurl-gnutls\\.so\\.[0-9]+.*$
%global __requires_exclude ^libcurl\\.so\\.[0-9]+.*$

%description
GitHub Desktop Plus is a graphical Git client for managing GitHub repositories easily.
This spec simply repackages the RPM for distribution via Copr.

%prep
# Nothing to build

%build
# Nothing to build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

## Strip invalid RPATHs and fix to link against system libcurl
for bin in %{buildroot}/usr/lib/%{name}/resources/app/git/libexec/git-core/git-*; do
    if file "$bin" | grep -q ELF; then
        chrpath -d "$bin" || true
        patchelf --replace-needed libcurl-gnutls.so.4 libcurl.so.4 "$bin" || true
    fi
done

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
/usr/lib/%{name}/**
/usr/share/doc/%{name}/copyright

%changelog
%autochangelog
