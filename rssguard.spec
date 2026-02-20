### ref: https://github.com/fedora-riscv/rssguard/blob/main/rssguard.spec
# https://github.com/flathub/io.github.martinrotter.rssguard/blob/master/io.github.martinrotter.rssguard.yml
### rssguard-5 remove builtin web browser, so do not use `NO_LITE` option. https://rssguard.readthedocs.io/en/latest/5-vs-4.html

Name:           rssguard
Version:        5.0.0
Release:        %autorelease
Summary:        Simple yet powerful feed reader

License:        GPL-3.0-or-later AND BSD-3-Clause
URL:            https://github.com/martinrotter/rssguard
Source0:        %{url}/archive/%{version}/rssguard-%{version}.tar.gz

%global         dev_version 3e7bdfd58
Source0:        %{url}/releases/download/devbuild5/rssguard-dev-%{dev_version}-src.tar.gz

%global debug_package %{nil}

BuildRequires:  cmake gcc-c++
BuildRequires:  qt6-qtbase-devel qt6-qttools-devel qt6-qtwebengine-devel qt6-qtwebchannel-devel
BuildRequires:  qt6-qt5compat-devel qt6-linguist qt6-qtmultimedia-devel qt6-qtbase-private-devel
BuildRequires:  libappstream-glib desktop-file-utils mpv-devel sqlite-devel
BuildRequires:  golang

Requires:       rssguard-extractor = %{version}

%description
RSS Guard is simple, light and easy-to-use RSS/ATOM feed aggregator developed using the Qt framework which supports online feed synchronization.

%package extractor
Summary: Article extractor for RSS Guard
Requires: %{name}%{?_isa} = %{version}-%{release}

%description extractor
Standalone article extraction helper for RSS Guard.

%prep
### rssguard-%{version}  rssguard-dev
%autosetup -n rssguard-dev-%{dev_version}

%build
%cmake -DBUILD_WITH_QT6=ON \
    -DENABLE_COMPRESSED_SITEMAP=ON \
    -DENABLE_MEDIAPLAYER_LIBMPV=ON \
    -DENABLE_MEDIAPLAYER_QTMULTIMEDIA=OFF \
    -DFORCE_BUNDLE_ICONS=OFF \
    -DNO_UPDATE_CHECK=ON
%cmake_build

## clean up /lib/*.a files
find . -name "/lib/*.a" -type f -delete

%install
%cmake_install

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/*.xml

%files
%doc README.md
%license LICENSE.md
%{_bindir}/rssguard
%{_datadir}/applications/io.github.martinrotter.rssguard.desktop
%{_datadir}/icons/hicolor/*/apps/io.github.martinrotter.rssguard.png
%{_datadir}/metainfo/io.github.martinrotter.rssguard.metainfo.xml
%{_libdir}/librssguard.so
%{_libdir}/rssguard/*.so
%{_includedir}/librssguard/

%files extractor
%{_bindir}/rssguard-article-extractor

%changelog
%autochangelog
