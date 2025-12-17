### ref: https://github.com/terrapkg/packages/blob/frawhide/anda/devs/zed/stable/zed.spec
### Use tarball to avoid building time.

Name:           zed
Version:        0.217.1
Release:        1%{?dist}
Summary:        High-performance, multiplayer code editor

License:        AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://github.com/zed-industries/zed
Source0:        %{url}/releases/download/v%{version}/zed-linux-x86_64.tar.gz

# Disable debug package
%define debug_package %{nil}
%define __strip /bin/true

%description
Code at the speed of thought — Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.

%prep
%autosetup -n zed.app

%build
# Nothing to build (precompiled)

%install
### Install the whole bundle under /usr/libexec/zed
mkdir -p %{buildroot}%{_libexecdir}/zed
cp -r bin lib libexec licenses.md share %{buildroot}%{_libexecdir}/zed/

### Symlink main executable
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/zed/bin/zed %{buildroot}%{_bindir}/zed

### Desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/zed.desktop <<'EOF'
[Desktop Entry]
Name=Zed
GenericName=Text Editor
Exec=zed %U
Icon=zed
Type=Application
StartupNotify=true
Categories=Utility;TextEditor;Development;IDE;
MimeType=text/plain;application/x-zerosize;x-scheme-handler/zed;
Actions=NewWorkspace;
Keywords=zed;
StartupWMClass=dev.zed.Zed

[Desktop Action NewWorkspace]
Name=Open a new workspace
Exec=zed --new %U
EOF

### Create "Open with" menu
mkdir -p %{buildroot}%{_datadir}/kio/servicemenus
cat > %{buildroot}%{_datadir}/kio/servicemenus/open_in_zed.desktop <<'EOF'
[Desktop Entry]
Type=Service
ServiceTypes=KonqPopupMenu/Plugin
MimeType=inode/directory;
X-KDE-Priority=TopLevel
Actions=openInZed
X-KDE-StartupNotify=false

[Desktop Action openInZed]
Name=Open in Zed
Icon=zed
Exec=zed %u
EOF

### Install icons (already in correct structure)
cp -r share/icons %{buildroot}%{_datadir}/

%files
%license %{_libexecdir}/zed/licenses.md
%{_bindir}/zed
%{_libexecdir}/zed/
%{_datadir}/applications/zed.desktop
%{_datadir}/kio/servicemenus/open_in_zed.desktop
%{_datadir}/icons/hicolor/*/apps/zed.png

%changelog
%autochangelog
