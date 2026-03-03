### Note: FreeFileSync’s installer requires a terminal (tty) and cannot run headlessly.
    # Don’t execute the '.run' installer in Copr (fails without a terminal). Use '--keep --noexec' to unpack its contents.
    # Manually install files into %{buildroot} using 'install/cp'.

Name:       freefilesync
Version:    14.6
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

archive_line=$(awk '/^__ARCHIVE_BELOW__$/ {print NR + 1; exit}' "${installer}")
if [ -z "${archive_line}" ]; then
    archive_line=$(awk -F= '/^SKIP=/{gsub(/[^0-9]/, "", $2); print $2; exit}' "${installer}")
fi
test -n "${archive_line}"

compress=$(awk -F= '/^COMPRESS=/{gsub(/["[:space:]]/, "", $2); print tolower($2); exit}' "${installer}")

case "${compress}" in
    xz)
        tail -n +"${archive_line}" "${installer}" | tar -xJf - -C "${extract_dir}"
        ;;
    bzip2|bz2)
        tail -n +"${archive_line}" "${installer}" | tar -xjf - -C "${extract_dir}"
        ;;
    gzip|gz|pigz|"")
        tail -n +"${archive_line}" "${installer}" | tar -xzf - -C "${extract_dir}"
        ;;
    *)
        echo "Unsupported installer compression: ${compress}" >&2
        exit 1
        ;;
esac

### Binaries
install -Dpm755 ffs-extracted/FreeFileSync/FreeFileSync \
    %{buildroot}%{_bindir}/FreeFileSync
install -Dpm755 ffs-extracted/FreeFileSync/RealTimeSync \
    %{buildroot}%{_bindir}/RealTimeSync

### Desktop entries
install -Dpm644 ffs-extracted/FreeFileSync/FreeFileSync.desktop \
    %{buildroot}%{_datadir}/applications/FreeFileSync.desktop
install -Dpm644 ffs-extracted/FreeFileSync/RealTimeSync.desktop \
    %{buildroot}%{_datadir}/applications/RealTimeSync.desktop

### Resources
mkdir -p %{buildroot}%{_datadir}/freefilesync
cp -a ffs-extracted/FreeFileSync/Resources \
    %{buildroot}%{_datadir}/freefilesync/

### Icons
cp -a ffs-extracted/FreeFileSync/Icons/* \
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