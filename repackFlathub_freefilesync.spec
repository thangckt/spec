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
%setup -q -n FreeFileSync_%{version}_Linux_x86_64

%build
# No compilation needed; the application is precompiled.

%install
# Install the FreeFileSync binaries
mkdir -p %{buildroot}/%{_bindir}
cp -a Bin/* %{buildroot}/%{_bindir}/

# Install desktop entries
mkdir -p %{buildroot}/%{_datadir}/applications
cp -a *.desktop %{buildroot}/%{_datadir}/applications/

# Install icons
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps
cp -a *.png %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/

# Install appdata XML
mkdir -p %{buildroot}/%{_datadir}/appdata
cp -a *.appdata.xml %{buildroot}/%{_datadir}/appdata/

%files
%{_bindir}/FreeFileSync
%{_bindir}/RealTimeSync
%{_datadir}/applications/org.freefilesync.FreeFileSync.desktop
%{_datadir}/applications/org.freefilesync.FreeFileSync.RealTimeSync.desktop
%{_datadir}/icons/hicolor/128x128/apps/org.freefilesync.FreeFileSync.png
%{_datadir}/icons/hicolor/128x128/apps/org.freefilesync.FreeFileSync.RealTimeSync.png
%{_datadir}/appdata/org.freefilesync.FreeFileSync.appdata.xml

%changelog
%autochangelog
