Name:           freefilesync
Version:        14.5
Release:        1%{?dist}
Summary:        Open-source file synchronization and backup software

License:        GPL-3.0-or-later
URL:            https://github.com/flathub/org.freefilesync.FreeFileSync
Source0:        %{url}/releases/download/reupload-%{version}/FreeFileSync_%{version}_Linux_x86_64.tar.gz


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
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
tar -xzf %{SOURCE0} -C %{name}-%{version}

%build
# No compilation needed; the application is precompiled.

%install
# Create install directories
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_datadir}/metainfo

# Copy binaries
install -m 0755 FreeFileSync %{buildroot}%{_bindir}/FreeFileSync
install -m 0755 RealTimeSync %{buildroot}%{_bindir}/RealTimeSync

# Copy desktop files
install -m 0644 FreeFileSync.desktop %{buildroot}%{_datadir}/applications/
install -m 0644 RealTimeSync.desktop %{buildroot}%{_datadir}/applications/

# Copy icons
install -m 0644 Resources/FreeFileSync.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
install -m 0644 Resources/RealTimeSync.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/

# Copy AppData (metainfo)
install -m 0644 org.freefilesync.FreeFileSync.appdata.xml %{buildroot}%{_datadir}/metainfo/

%files
%license License.txt
%doc Readme.txt
%{_bindir}/FreeFileSync
%{_bindir}/RealTimeSync
%{_datadir}/applications/FreeFileSync.desktop
%{_datadir}/applications/RealTimeSync.desktop
%{_datadir}/icons/hicolor/128x128/apps/FreeFileSync.png
%{_datadir}/icons/hicolor/128x128/apps/RealTimeSync.png
%{_datadir}/metainfo/org.freefilesync.FreeFileSync.appdata.xml

%changelog
%autochangelog
