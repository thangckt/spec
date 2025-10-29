### ref: https://github.com/fedora-riscv/rssguard/blob/main/rssguard.spec
# https://github.com/flathub/io.github.martinrotter.rssguard/blob/master/io.github.martinrotter.rssguard.yml

Name:           rssguard
Version:        4.8.6
Release:        %autorelease
Summary:        Simple yet powerful feed reader

License:        GPL-3.0-or-later AND BSD-3-Clause
URL:            https://github.com/martinrotter/rssguard
Source0:        %{url}/archive/%{version}/rssguard-%{version}.tar.gz

ExclusiveArch:  %{qt6_qtwebengine_arches}

BuildRequires:  cmake gcc-c++
BuildRequires:  qt6-qtbase-devel qt6-qttools-devel qt6-qtwebengine-devel qt6-qtwebchannel-devel
BuildRequires:  qt6-qt5compat-devel qt6-linguist qt6-qtmultimedia-devel
BuildRequires:  libappstream-glib desktop-file-utils mpv-devel sqlite-devel

%description
RSS Guard is simple, light and easy-to-use RSS/ATOM feed aggregator developed using the Qt framework which supports online feed synchronization.

%prep
%autosetup -n rssguard-%{version}

%build
%cmake -DBUILD_WITH_QT6=ON \
    -DENABLE_COMPRESSED_SITEMAP=ON \
    -DENABLE_MEDIAPLAYER_LIBMPV=ON \
    -DENABLE_MEDIAPLAYER_QTMULTIMEDIA=OFF \
    -DFORCE_BUNDLE_ICONS=OFF \
    -DNO_LITE=ON  \
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

# Main app binary
%{_bindir}/%{name}

# Application desktop integration
%{_datadir}/applications/io.github.martinrotter.rssguard.desktop
%{_datadir}/icons/hicolor/*/apps/io.github.martinrotter.rssguard.png
%{_datadir}/metainfo/io.github.martinrotter.rssguard.metainfo.xml

# Shared library
%{_libdir}/librssguard.so
%{_libdir}/rssguard/*.so

# Development headers
%{_includedir}/librssguard/

%changelog
%autochangelog