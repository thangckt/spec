### Revise by Gemini to build all three components in a single spec file, which includes:
## - evolution-data-server (EDS): https://src.fedoraproject.org/rpms/evolution-data-server/blob/rawhide/f/evolution-data-server.spec
## - evolution: https://src.fedoraproject.org/rpms/evolution/blob/rawhide/f/evolution.spec
## - evolution-ews: https://src.fedoraproject.org/rpms/evolution-ews/blob/rawhide/f/evolution-ews.spec


Name:           evolution
Version:        3.61.1
Release:        1%{?dist}
Summary:        GNOME Evolution Suite
License:        GPL-2.0-or-later
URL:            https://gitlab.gnome.org/GNOME/evolution

Source0:        https://gitlab.gnome.org/GNOME/evolution/-/archive/%{version}/evolution-%{version}.tar.gz
Source1:        https://gitlab.gnome.org/GNOME/evolution-data-server/-/archive/%{version}/evolution-data-server-%{version}.tar.gz
Source2:        https://gitlab.gnome.org/GNOME/evolution-ews/-/archive/%{version}/evolution-ews-%{version}.tar.gz

BuildRequires:  cmake gcc gcc-c++ pkgconfig gettext gperf vala intltool itstool
BuildRequires:  gtk4-devel webkitgtk6.0-devel webkit2gtk4.1-devel
BuildRequires:  gnome-online-accounts-devel gnome-autoar-devel gnome-desktop3-devel gsettings-desktop-schemas-devel
BuildRequires:  nss-devel yelp-tools openldap-devel gspell-devel
BuildRequires:  libsecret-devel libgweather4-devel libcanberra-devel libnotify-devel libuuid-devel libical-devel libical-glib-devel
BuildRequires:  gdk-pixbuf2-devel highlight libpst-devel libarchive-devel libnma-devel libytnef-devel
BuildRequires:  libmspack libmspack-devel

%global __brp_compress true
%global __brp_mangle_shebangs true

%description
This spec builds all Evolution components in a unified build process, including Evolution Data Server (EDS), Evolution, and Evolution EWS plugin.

### Subpackage: evolution-data-server
%package -n evolution-data-server
Summary:        GNOME Evolution Data Server
License:        GPL-2.0-or-later

%description -n evolution-data-server
This spec builds Evolution Data Server (EDS), which is a set of libraries and services.

### Subpackage: evolution-ews
%package -n evolution-ews
Summary:        GNOME Evolution EWS plugin
License:        GPL-2.0-or-later
Requires:       evolution >= %{version}

%description -n evolution-ews
This spec builds Evolution EWS plugin.


%prep
### Create a top-level directory and extract all sources manually to keep it clean
%setup -q -c -T
tar -xf %{SOURCE0}
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}

%build
export CFLAGS="%{optflags} -fPIC -Wno-sign-compare -Wno-deprecated-declarations -flto"
export CXXFLAGS="$CFLAGS"

rm -rf %{buildroot}
mkdir -p %{buildroot}

### Explicitly map our pkg-config and cmake environments to the standard buildroot target
STAGING_PKGCONFIG="%{buildroot}%{_libdir}/pkgconfig:%{buildroot}%{_datadir}/pkgconfig"

################ANCHOR 1. Build Evolution Data Server
cd evolution-data-server-%{version}
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DWITH_SYSTEMDUSERUNITDIR=%{_userunitdir} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
    -DWITH_LIBDB=OFF -DENABLE_GTK_DOC=OFF \
    -DENABLE_OAUTH2_WEBKITGTK=ON -DENABLE_OAUTH2_WEBKITGTK4=ON \
    -DENABLE_GTK=ON
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..

### Snapshot of what EDS installed - baseline for diffing later stages
find %{buildroot} -type f | sed "s|^%{buildroot}||" | sort > eds_files.txt

################ANCHOR 2. Build Evolution
cd evolution-%{version}
### Inject buildroot into the path so it detects the newly built libraries/headers
env PKG_CONFIG_LIBDIR="$STAGING_PKGCONFIG" PKG_CONFIG_PATH= \
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_PREFIX_PATH="%{buildroot}%{_prefix}" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
    -DENABLE_PLUGINS=all \
    -DENABLE_MAINTAINER_MODE=OFF \
    -DENABLE_GTK_DOC=OFF \
    -DENABLE_MARKDOWN=OFF
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..

### Files added since the EDS snapshot = Evolution's own files
find %{buildroot} -type f | sed "s|^%{buildroot}||" | sort > after_evolution.txt
comm -13 eds_files.txt after_evolution.txt > evolution_files.txt

################ANCHOR 3. Build Evolution EWS
cd evolution-ews-%{version}
env PKG_CONFIG_LIBDIR="$STAGING_PKGCONFIG" PKG_CONFIG_PATH= \
%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_PREFIX_PATH="%{buildroot}%{_prefix}" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir}
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..

### Files added since the Evolution snapshot = EWS's own files
find %{buildroot} -type f | sed "s|^%{buildroot}||" | sort > after_ews.txt
comm -13 after_evolution.txt after_ews.txt > ews_files.txt


%install
### Everything was already installed straight into %{buildroot} during %build via DESTDIR=%{buildroot} %cmake_install for each component.
### There is nothing left to install here, and critically: do NOT rm -rf %{buildroot} in this section
###
### eds_files.txt / evolution_files.txt / ews_files.txt were generated in %build by diffing buildroot snapshots taken after each
### component's install step, so they're derived from what was actually installed rather than guessed via path-pattern grep.


%files -f evolution_files.txt

%files -n evolution-data-server -f eds_files.txt

%files -n evolution-ews -f ews_files.txt

%changelog
%autochangelog