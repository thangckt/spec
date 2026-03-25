### REF: https://gitlab.com/athenaos/packages/applications/vscodium/-/blob/main/rpm/vscodium.spec?ref_type=heads
### https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo
### Use tarball to avoid building time.

%global vscode_arch x64
%global debug_package %{nil}

Name:           codium
Version:        1.112.01907
Release:        1%{?dist}
Summary:        Free/Libre Open Source Software Binaries of VSCode

License:        MIT
URL:            https://github.com/VSCodium/vscodium
Source0:        %{url}/releases/download/%{version}/VSCodium-linux-%{vscode_arch}-%{version}.tar.gz

## Filter out the problematic dependency: `libcurl.so.4(CURL_OPENSSL_4)(64bit)`


%description
VSCodium is a community-driven, freely-licensed binary distribution of Microsoft's VS Code.

%prep
%setup -c -n VSCodium-linux-%{vscode_arch}-%{version}

%build
# Nothing to build (precompiled)

%install
### Install the whole bundle under /usr/libexec/vscodium
mkdir -p %{buildroot}%{_libexecdir}/vscodium
cp -r * %{buildroot}%{_libexecdir}/vscodium/

### Symlink main executable
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libexecdir}/vscodium/bin/codium %{buildroot}%{_bindir}/codium

### Desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=VSCodium
GenericName=Text Editor
Exec=/usr/bin/codium %F
Icon=%{name}
Type=Application
StartupNotify=true
Categories=Utility;Development;IDE;
MimeType=text/plain;inode/directory;application/x-code-workspace;
Actions=new-empty-window;
Keywords=vscode;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=/usr/bin/codium --new-window %F
Icon=%{name}
EOF

### Create "Open with" menu
mkdir -p %{buildroot}%{_datadir}/kio/servicemenus
cat > %{buildroot}%{_datadir}/kio/servicemenus/open_in_codium.desktop <<'EOF'
[Desktop Entry]
Type=Service
ServiceTypes=KonqPopupMenu/Plugin
MimeType=inode/directory;
X-KDE-Priority=TopLevel
Actions=openInCodium
X-KDE-StartupNotify=false

[Desktop Action openInCodium]
Name=Open in Codium
Icon=codium
Exec=codium %u
EOF

### Icon
install -D -m644 resources/app/resources/linux/code.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png


%files
%{_bindir}/codium
%{_libexecdir}/vscodium
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

%changelog
%autochangelog
