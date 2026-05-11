### goldendict-ng is actively maintained fork of goldendict with new features and bug fixes
### Build from source: https://xiaoyifang.github.io/goldendict-ng/howto/build_from_source/

Name:           goldendict-ng
Version:        26.5.4
Release:        1%{?dist}
Summary:        Feature-rich dictionary lookup program

License:        GPL-3.0-or-later
URL:            https://github.com/xiaoyifang/goldendict-ng
Source0:        %{url}/archive/refs/tags/v%{version}-Release.ea1a9803.tar.gz

BuildRequires:  gcc-c++ make pkgconfig git
BuildRequires:  hunspell-devel zlib-devel bzip2-devel lzo-devel eb-devel
BuildRequires:  libvorbis-devel libXtst-devel libavutil-free-devel libavformat-free-devel libzstd-devel
BuildRequires:  libxkbcommon-devel libzim-devel opencc-devel fmt-devel xapian-core-devel
BuildRequires:  qt6-qtbase-devel qt6-qtsvg-devel qt6-qtmultimedia-devel qt6-qt5compat-devel
BuildRequires:  qt6-qttools-devel qt6-qtspeech-devel qt6-qtwebchannel-devel qt6-qtwebengine-devel

Requires:       hunspell translate-shell mpg123

#  ffmpeg-free-devel libao-devel libtiff-devel

#  x11proto-record-dev

%description
GoldenDict is a feature-rich dictionary lookup program supporting multiple dictionary formats,
including Babylon, StarDict, Dictd, and others. It provides a modern Qt interface, support for
Wikipedia, and various offline/online resources.

%prep
%setup -q -n goldendict-ng-%{version}-Release.ea1a9803

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_DO_STRIP=ON
%cmake_build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications

# Install binary
install -m 0755 goldendict %{buildroot}%{_bindir}/goldendict

# Install .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=GoldenDict
GenericName=Multiformat Dictionary
Exec=goldendict
Icon=goldendict
Terminal=false
Type=Application
Categories=Education;Languages;
EOF

# Install icon manually (SVG preferred if available)
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp icons/programicon.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/goldendict.png

# Install help files
mkdir -p %{buildroot}%{_datadir}/goldendict/help
cp -a help/* %{buildroot}%{_datadir}/goldendict/help/

%files
%{_bindir}/goldendict
%{_datadir}/applications/goldendict.desktop
%{_datadir}/icons/hicolor/64x64/apps/goldendict.png
%{_datadir}/goldendict/help/

%changelog
%autochangelog