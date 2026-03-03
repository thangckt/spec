### Note: FreeFileSync’s installer requires a terminal (tty) and cannot run headlessly.
    # Don’t execute the '.run' installer in Copr (fails without a terminal). Use '--keep --noexec' to unpack its contents.
    # Manually install files into %{buildroot} using 'install/cp'.

Name:       freefilesync
Version:    14.8
Release:    1%{?dist}
Summary:    A file synchronization utility

License:    GPLv3
#RL:        http://www.freefilesync.org/
#RL:        https://github.com/flathub/org.freefilesync.FreeFileSync
URL:        https://github.com/hkneptune/FreeFileSync
Source0:    %{url}/releases/download/v%{version}/FreeFileSync_%{version}_Linux_x86_64.tar.gz

%define debug_package %{nil}
%define __strip /bin/true

%description
FreeFileSync is an open-source software that helps synchronize files and folders on Windows, Linux, and macOS.
This spec does not build from source, but only repacks the official precompiled Linux binaries.

%prep
tar -zxvf %{SOURCE0}

%build
# Nothing to build

%install
rm -rf %{buildroot}

### Extract installer payload WITHOUT executing the .run script (Copr-safe, no TTY required)
installer="FreeFileSync_%{version}_Install.run"
extract_dir="ffs-extracted"

mkdir -p "${extract_dir}"
chmod +x "${installer}"
env -u DISPLAY QT_QPA_PLATFORM=offscreen "./${installer}" \
    --accept-license \
    --skip-overview \
    --directory "${extract_dir}" \
    --for-all-users false \
    --create-shortcuts false

### Binaries
install -Dpm755 ffs-extracted/FreeFileSync \
    %{buildroot}%{_bindir}/FreeFileSync
install -Dpm755 ffs-extracted/RealTimeSync \
    %{buildroot}%{_bindir}/RealTimeSync

### Desktop entries
install -Dpm644 ffs-extracted/Resources/FreeFileSync.desktop \
    %{buildroot}%{_datadir}/applications/FreeFileSync.desktop
install -Dpm644 ffs-extracted/Resources/RealTimeSync.desktop \
    %{buildroot}%{_datadir}/applications/RealTimeSync.desktop

### Resources
mkdir -p %{buildroot}%{_datadir}/freefilesync
cp -a ffs-extracted/Resources \
    %{buildroot}%{_datadir}/freefilesync/

### Icons
cp -a ffs-extracted/Resources/Icons/* \
    %{buildroot}%{_datadir}/icons/hicolor/


%files
%license License.txt
%doc Changelog.txt
%{_bindir}/FreeFileSync
%{_bindir}/RealTimeSync
%{_datadir}/applications/FreeFileSync.desktop
%{_datadir}/applications/RealTimeSync.desktop
%{_datadir}/icons/hicolor/*x*/*/*.png
%{_datadir}/freefilesync

%changelog
%autochangelog


# ffs_name="FreeFileSync_14.3"
# tarfile="${ffs_name}_Linux.tar.gz"
# wget "https://freefilesync.org/download/$tarfile"
# tar -zxvf $tarfile
# ./${ffs_name}_Install.run