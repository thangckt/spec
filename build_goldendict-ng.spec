### goldendict-ng is actively maintained fork of goldendict with new features and bug fixes
### Build: https://xiaoyifang.github.io/goldendict-ng/howto/build_from_source/
### Wayland support: https://xiaoyifang.github.io/goldendict-ng/topic_wayland/
### https://src.fedoraproject.org/rpms/goldendict-ng/blob/rawhide/f/goldendict-ng.spec

Name:           goldendict-ng
Version:        26.6.1
Release:        1%{?dist}
Summary:        Feature-rich dictionary lookup program

License:        GPL-3.0-or-later
URL:            https://github.com/xiaoyifang/goldendict-ng
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc-c++ make pkgconfig git
BuildRequires:  hunspell-devel zlib-devel bzip2-devel lzo-devel eb-devel
BuildRequires:  libvorbis-devel libXtst-devel libavutil-free-devel libavformat-free-devel libzstd-devel
BuildRequires:  libxkbcommon-devel libzim-devel opencc-devel fmt-devel xapian-core-devel tomlplusplus-devel cups-devel
BuildRequires:  qt6-qtbase-devel qt6-qtsvg-devel qt6-qtmultimedia-devel qt6-qt5compat-devel
BuildRequires:  qt6-qttools-devel qt6-qtspeech-devel qt6-qtwebchannel-devel qt6-qtwebengine-devel

Requires:       hunspell translate-shell mpg123

%description
GoldenDict is a feature-rich dictionary lookup program supporting multiple dictionary formats,
including Babylon, StarDict, Dictd, and others. It provides a modern Qt interface, support for
Wikipedia, and various offline/online resources.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

### Install desktop file (exited)
mkdir -p %{buildroot}%{_datadir}/applications
mv %{buildroot}%{_datadir}/applications/io.github.xiaoyifang.goldendict_ng.desktop %{buildroot}%{_datadir}/applications/goldendict_ng.desktop

### Install Icon (48x48 or 64x64 is standard for PNG pixmaps)
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mv %{buildroot}%{_datadir}/pixmaps/goldendict.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/goldendict.png

### Delete metainfo
rm %{buildroot}%{_datadir}/metainfo/io.github.xiaoyifang.goldendict_ng.metainfo.xml

%files
%{_bindir}/goldendict
%{_datadir}/goldendict
%{_datadir}/applications/goldendict_ng.desktop
%{_datadir}/icons/hicolor/128x128/apps/goldendict.png

%changelog
%autochangelog
