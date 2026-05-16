### goldendict-ng is actively maintained fork of goldendict with new features and bug fixes
### Build: https://xiaoyifang.github.io/goldendict-ng/howto/build_from_source/
### Wayland support: https://xiaoyifang.github.io/goldendict-ng/topic_wayland/

Name:           goldendict-ng
Version:        26.5.5
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

%files
%{_bindir}/goldendict
%{_datadir}

%changelog
%autochangelog
