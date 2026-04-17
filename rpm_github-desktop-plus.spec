### DO NOT replace bundled git with system git. It will break the app.
### The bundled git is not pure git, it has customize with extra features.
## Gitlab push work well in version 3.5.4, but fail in version 3.5.5

Name:           github-desktop-plus
Version:        3.5.8.1
Release:        1%{?dist}
Summary:        GitHub Desktop Plus

License:        MIT
URL:            https://github.com/pol-rivero/github-desktop-plus
Source0:        %{url}/releases/download/v%{version}/GitHubDesktopPlus-v%{version}-linux-x86_64.rpm

BuildRequires:  chrpath, patchelf

### Filter out the problematic dependency: `libcurl-gnutls`
## 1. Filter the library files
%global __requires_exclude ^(libcurl-gnutls|libcurl|libjpeg)\.so\.[0-9]+.*$
## 2. Filter the specific versioned symbol that Fedora cannot provide
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^libcurl\.so\.4\(CURL_GNUTLS_3\)\(64bit\)$

%description
GitHub Desktop Plus is a graphical Git client for managing GitHub repositories easily.
This spec simply repackages the RPM for distribution via Copr.

%prep
# Nothing to build

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

## Strip invalid RPATHs and fix to link against system libcurl
for bin in %{buildroot}/usr/lib/%{name}/resources/app/git/libexec/git-core/git-*; do
    if file "$bin" | grep -q ELF; then
        chrpath -d "$bin" || true
        ## Fix libcurl
        patchelf --replace-needed libcurl-gnutls.so.4 libcurl.so.4 "$bin" || true
        ## Fix libjpeg 
        patchelf --replace-needed libjpeg.so.8 libjpeg.so.62 "$bin" || true
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
