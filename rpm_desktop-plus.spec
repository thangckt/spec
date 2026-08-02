### ### The Electron bundled git is a customized git with extra features.
### DO NOT replace bundled git with system git. It will break the app.
### Use 'AutoReqProv: no' to disable automatic dependency generation.

Name:           desktop-plus
Version:        3.6.4.2
Release:        1%{?dist}
Summary:        GitHub Desktop Plus

License:        MIT
URL:            https://github.com/DesktopPlus/desktop-plus
Source0:        %{url}/releases/download/v%{version}/DesktopPlus-v%{version}-linux-x86_64.rpm

BuildRequires:  chrpath, patchelf
Requires:       libcurl

AutoReqProv: no

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

### Strip invalid RPATHs and fix to link against system libcurl
for bin in %{buildroot}/usr/lib/%{name}/resources/app/git/libexec/git-core/git-*; do
    if file "$bin" | grep -q ELF; then
        chrpath -d "$bin" || true
        ## Fix libcurl and libjpeg
        patchelf --replace-needed libcurl-gnutls.so.4 libcurl.so.4 "$bin" || true
        patchelf --replace-needed libjpeg.so.8 libjpeg.so.62 "$bin" || true
    fi
done

### Fix ClassName in desktop-plus.desktop
# if [ -f "%{buildroot}%{_datadir}/applications/%{name}.desktop" ]; then
#     if grep -q '^StartupWMClass=' "%{buildroot}%{_datadir}/applications/%{name}.desktop"; then
#         sed -i 's/^StartupWMClass=.*/StartupWMClass=desktop-plus/' "%{buildroot}%{_datadir}/applications/%{name}.desktop"
#     else
#         sed -i '$a\' "%{buildroot}%{_datadir}/applications/%{name}.desktop"
#         echo "StartupWMClass=desktop-plus" >> "%{buildroot}%{_datadir}/applications/%{name}.desktop"
#     fi

#     sed -i 's/GitHub;//g' %{buildroot}%{_datadir}/applications/desktop-plus.desktop
# fi

### Remove unnecessary files to reduce package size
find %{buildroot} -name "*.bak" -delete

%files
%{_bindir}/%{name}
/usr/lib/%{name}/
%{_datadir}/doc/%{name}/copyright
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/gh-desktop-plus.png

%changelog
%autochangelog
