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

### Multi-source definition
Source0:        https://gitlab.gnome.org/GNOME/evolution/-/archive/%{version}/evolution-%{version}.tar.gz
Source1:        https://gitlab.gnome.org/GNOME/evolution-data-server/-/archive/%{version}/evolution-data-server-%{version}.tar.gz
Source2:        https://gitlab.gnome.org/GNOME/evolution-ews/-/archive/%{version}/evolution-ews-%{version}.tar.gz

### Consolidated BuildRequires from all three specs
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
export CFLAGS="$RPM_OPT_FLAGS -fPIC -Wno-sign-compare -Wno-deprecated-declarations -flto"
export CPPFLAGS="-I%{_includedir}/et -flto"

mkdir -p %{buildroot}

### Explicitly map our pkg-config and cmake environments to the standard buildroot target
STAGING_PKG_CONFIG="%{buildroot}%{_libdir}/pkgconfig:%{buildroot}%{_datadir}/pkgconfig"

################ANCHOR 1. Build Evolution Data Server
cd evolution-data-server-%{version}
%cmake \
    -DWITH_SYSTEMDUSERUNITDIR=%{_userunitdir} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
    -DWITH_LIBDB=OFF -DENABLE_GTK_DOC=OFF \
    -DENABLE_OAUTH2_WEBKITGTK=ON -DENABLE_OAUTH2_WEBKITGTK4=ON \
    -DENABLE_GTK=ON
%cmake_build
### Install immediately into the buildroot
DESTDIR="%{buildroot}" %cmake_install
cd ..

################ANCHOR 2. Build Evolution
cd evolution-%{version}

# CRITICAL FIX: Erase any global macro cache inherited from the prior run
rm -rf "%{_vpath_builddir}"

### Inject buildroot into the path so it detects the newly built libraries/headers
env PKG_CONFIG_PATH="$STAGING_PKG_CONFIG:$PKG_CONFIG_PATH" \
%cmake \
    -DCMAKE_PREFIX_PATH="%{buildroot}/usr" \
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
### Install immediately into the buildroot
DESTDIR="%{buildroot}" %cmake_install
cd ..

################ANCHOR 3. Build Evolution EWS
cd evolution-ews-%{version}

# CRITICAL FIX: Erase any global macro cache inherited from the prior run
rm -rf "%{_vpath_builddir}"

env PKG_CONFIG_PATH="$STAGING_PKG_CONFIG:$PKG_CONFIG_PATH" \
%cmake \
    -DCMAKE_PREFIX_PATH="%{buildroot}/usr" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir}
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..


%install
### Clear buildroot and copy everything from our unified staging directory
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a %{_builddir}/_staging/* %{buildroot}/

### Generate separate file lists dynamically based on directory mappings
### Evolution Data Server files
find %{buildroot} -type f | grep -E "evolution-data-server|lib.*\.so|/usr/lib/systemd/" > eds_files.txt
sed -i "s|^%{buildroot}||" eds_files.txt

### Evolution EWS files
find %{buildroot} -type f | grep -E "evolution-ews|ews" > ews_files.txt
sed -i "s|^%{buildroot}||" ews_files.txt

### Main Evolution files (everything else)
find %{buildroot} -type f > all_files.txt
sed -i "s|^%{buildroot}||" all_files.txt
grep -Fvx -f eds_files.txt all_files.txt | grep -Fvx -f ews_files.txt > evolution_files.txt


%files -f evolution_files.txt

%files -n evolution-data-server -f eds_files.txt
%{_libdir}/lib*

%files -n evolution-ews -f ews_files.txt

%changelog
%autochangelog