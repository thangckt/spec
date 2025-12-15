### Note: FreeFileSync’s installer requires a terminal (tty) and cannot run headlessly.
    # Don’t execute the '.run' installer in Copr (fails without a terminal). Use '--keep --noexec' to unpack its contents.
    # Manually install files into %{buildroot} using 'install/cp'.

Name:       freefilesync
Version:    14.6
Release:    1%{?dist}
Summary:    A file synchronization utility

License:    GPLv3
#RL:        http://www.freefilesync.org/
URL:        https://github.com/flathub/org.freefilesync.FreeFileSync
Source0:    %{url}/releases/download/reupload-%{version}/FreeFileSync_%{version}_Linux_x86_64.tar.gz

# Disable debug package
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
./FreeFileSync_%{version}_Install.run --noexec --keep

# Binaries
install -Dpm755 FreeFileSync_extracted/FreeFileSync/FreeFileSync   %{buildroot}%{_bindir}/FreeFileSync
install -Dpm755 FreeFileSync_extracted/FreeFileSync/RealTimeSync   %{buildroot}%{_bindir}/RealTimeSync

# Desktop entries
install -Dpm644 FreeFileSync_extracted/FreeFileSync/FreeFileSync.desktop  %{buildroot}%{_datadir}/applications/FreeFileSync.desktop
install -Dpm644 FreeFileSync_extracted/FreeFileSync/RealTimeSync.desktop  %{buildroot}%{_datadir}/applications/RealTimeSync.desktop

# Icons and resources
cp -a FreeFileSync_extracted/FreeFileSync/Resources %{buildroot}%{_datadir}/freefilesync/
cp -a FreeFileSync_extracted/FreeFileSync/Icons/*   %{buildroot}%{_datadir}/icons/hicolor/


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