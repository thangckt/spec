Name:           freefilesync
Version:        14.5
Release:        1%{?dist}
Summary:        Open-source file synchronization and backup software

License:        GPL-3.0-or-later
URL:            https://github.com/flathub/org.freefilesync.FreeFileSync
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gtk2-devel
BuildRequires:  wxGTK3
BuildRequires:  p7zip
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

%description
FreeFileSync is a folder comparison and synchronization software that creates and manages backup copies of your important files.

%prep
# Extract the source tarball
rm -rf extractdir
mkdir -p extractdir
tar -xzf %{SOURCE0} -C extractdir

# At this point, we have a single file FreeFileSync-14.5-Install.run
chmod +x FreeFileSync-%{version}-Install.run

# Extract its contents without running installation
./FreeFileSync-%{version}-Install.run --target ./extracted --noexec

%build
# No compilation needed; the binaries are prebuilt.

%install
cd extracted

# Create install directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -d %{buildroot}%{_datadir}/metainfo

# Copy binaries
install -m 0755 FreeFileSync %{buildroot}%{_bindir}/FreeFileSync
install -m 0755 RealTimeSync %{buildroot}%{_bindir}/RealTimeSync

# Copy desktop files
install -m 0644 FreeFileSync.desktop %{buildroot}%{_datadir}/applications/
install -m 0644 RealTimeSync.desktop %{buildroot}%{_datadir}/applications/

# Copy icons
install -m 0644 Resources/FreeFileSync.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
install -m 0644 Resources/RealTimeSync.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/

# Copy AppData (if exists)
if [ -f org.freefilesync.FreeFileSync.appdata.xml ]; then
    install -m 0644 org.freefilesync.FreeFileSync.appdata.xml %{buildroot}%{_datadir}/metainfo/
fi

# Copy documentation
install -d %{buildroot}%{_docdir}/%{name}
cp -p Readme.txt %{buildroot}%{_docdir}/%{name}/
cp -p License.txt %{buildroot}%{_docdir}/%{name}/

%files
%license %{_docdir}/%{name}/License.txt
%doc %{_docdir}/%{name}/Readme.txt
%{_bindir}/FreeFileSync
%{_bindir}/RealTimeSync
%{_datadir}/applications/FreeFileSync.desktop
%{_datadir}/applications/RealTimeSync.desktop
%{_datadir}/icons/hicolor/128x128/apps/FreeFileSync.png
%{_datadir}/icons/hicolor/128x128/apps/RealTimeSync.png
%{_datadir}/metainfo/org.freefilesync.FreeFileSync.appdata.xml

%changelog
%autochangelog
