### Note: FreeFileSync’s installer requires a terminal (tty) and cannot run headlessly.
    # Don’t execute the '.run' installer in Copr (fails without a terminal).
    # This spec reivse by GPT-codex-5.3, when ask it to refer Fflatpak approach.

Name:       freefilesync
Version:        14.8
Release:    1%{?dist}
Summary:    A file synchronization utility

License:    GPLv3
#RL:        http://www.freefilesync.org/
#RL:        https://github.com/flathub/org.freefilesync.FreeFileSync
URL:        https://github.com/hkneptune/FreeFileSync
Source0:    %{url}/releases/download/v%{version}/FreeFileSync_%{version}_Linux_x86_64.tar.gz

%define debug_package %{nil}
%define __strip /bin/true

BuildRequires: 7zip

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
installer_dir="ffs-installer"

mkdir -p "${extract_dir}"
mkdir -p "${installer_dir}"

7z x -o"${installer_dir}" "${installer}" >/dev/null
tar -xzf "${installer_dir}/FreeFileSync.tar.gz" -C "${extract_dir}"

### Binaries
install -d %{buildroot}%{_libexecdir}/freefilesync
cp -a ffs-extracted/. %{buildroot}%{_libexecdir}/freefilesync/

cat > FreeFileSync <<'EOF'
#!/bin/sh
exec %{_libexecdir}/freefilesync/FreeFileSync "$@"
EOF
install -Dpm755 FreeFileSync %{buildroot}%{_bindir}/FreeFileSync

cat > RealTimeSync <<'EOF'
#!/bin/sh
exec %{_libexecdir}/freefilesync/RealTimeSync "$@"
EOF
install -Dpm755 RealTimeSync %{buildroot}%{_bindir}/RealTimeSync

### Desktop entries
sed \
    -e 's|Exec="FFS_INSTALL_PATH/FreeFileSync" %F|Exec=FreeFileSync %F|' \
    -e 's|Icon=FFS_INSTALL_PATH/Resources/FreeFileSync.png|Icon=FreeFileSync|' \
    "${installer_dir}/FreeFileSync.template.desktop" \
    > FreeFileSync.desktop
install -Dpm644 FreeFileSync.desktop \
    %{buildroot}%{_datadir}/applications/FreeFileSync.desktop

sed \
    -e 's|Exec="FFS_INSTALL_PATH/RealTimeSync" %F|Exec=RealTimeSync %F|' \
    -e 's|Icon=FFS_INSTALL_PATH/Resources/RealTimeSync.png|Icon=RealTimeSync|' \
    "${installer_dir}/RealTimeSync.template.desktop" \
    > RealTimeSync.desktop
install -Dpm644 RealTimeSync.desktop \
    %{buildroot}%{_datadir}/applications/RealTimeSync.desktop

### Icons
for res in 16 24 32 48 64 128 256; do
    install -Dpm644 "${installer_dir}/FreeFileSync-icon/${res}.png" \
        %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/FreeFileSync.png
    install -Dpm644 "${installer_dir}/RealTimeSync-icon/${res}.png" \
        %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/RealTimeSync.png
done

install -Dpm644 ffs-extracted/LICENSE \
    %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dpm644 ffs-extracted/CHANGELOG \
    %{buildroot}%{_docdir}/%{name}/CHANGELOG


%files
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_docdir}/%{name}/CHANGELOG
%{_bindir}/FreeFileSync
%{_bindir}/RealTimeSync
%{_libexecdir}/freefilesync
%{_datadir}/applications/FreeFileSync.desktop
%{_datadir}/applications/RealTimeSync.desktop
%{_datadir}/icons/hicolor/*x*/*/*.png

%changelog
%autochangelog
