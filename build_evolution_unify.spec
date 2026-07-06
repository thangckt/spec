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
%global __check_buildroot %{nil}
%global __brp_check_rpaths %{nil}

%description
This spec builds all Evolution components, including Evolution Data Server (EDS), Evolution, and Evolution EWS plugin.

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

### Subpackage: evolution-devel
%package devel
Summary:        Development files for GNOME Evolution Suite
License:        GPL-2.0-or-later
Requires:       evolution = %{version}-%{release}
Requires:       evolution-data-server = %{version}-%{release}

%description devel
Development files and headers for building extensions against Evolution and Evolution Data Server.


%prep
### Create a top-level directory and extract all sources manually to keep it clean
%setup -q -c -T
tar -xf %{SOURCE0}
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}


%build
rm -rf %{buildroot}
mkdir -p %{buildroot}

### Set up the search paths to look into our buildroot first
export PKG_CONFIG_PATH="%{buildroot}%{_libdir}/pkgconfig:%{buildroot}%{_datadir}/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="%{buildroot}%{_libdir}:$LD_LIBRARY_PATH"

### Standardize compiler and linker flags to find libraries in the buildroot
export CFLAGS="%{optflags} -I%{buildroot}%{_includedir}"
export CXXFLAGS="%{optflags} -I%{buildroot}%{_includedir}"
export LDFLAGS="%{__global_ldflags} -L%{buildroot}%{_libdir}"

################ANCHOR 1. Build Evolution Data Server
cd evolution-data-server-%{version}
%cmake \
    -DWITH_SYSTEMDUSERUNITDIR=%{_userunitdir} \
    -DWITH_LIBDB=OFF \
    -DENABLE_GTK_DOC=OFF \
    -DENABLE_OAUTH2_WEBKITGTK=ON \
    -DENABLE_OAUTH2_WEBKITGTK4=ON \
    -DENABLE_GTK=ON
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..

################ANCHOR 2. Build Evolution
cd evolution-%{version}
%cmake \
    -DCMAKE_PREFIX_PATH="%{buildroot}%{_prefix}" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath-link,%{buildroot}%{_libdir} -Wl,-rpath-link,%{buildroot}%{_libdir}/evolution-data-server" \
    -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath-link,%{buildroot}%{_libdir} -Wl,-rpath-link,%{buildroot}%{_libdir}/evolution-data-server" \
    -DENABLE_PLUGINS=all \
    -DENABLE_MAINTAINER_MODE=OFF \
    -DENABLE_GTK_DOC=OFF \
    -DENABLE_MARKDOWN=OFF
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..

################ANCHOR 3. Build Evolution EWS
cd evolution-ews-%{version}
%cmake \
    -DCMAKE_PREFIX_PATH="%{buildroot}%{_prefix}" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DEVO_PLUGIN_DIR="%{buildroot}%{_libdir}/evolution/modules" \
    -DEDS_MODULE_DIR="%{buildroot}%{_libdir}/evolution-data-server"
%cmake_build
DESTDIR="%{buildroot}" %cmake_install
cd ..


%install
### Note: Do NOT recreate %{buildroot} or wipe it here, since we installed everything into it during %build

### Remove all help documentation languages except English (C)
find %{buildroot}%{_datadir}/help/ -mindepth 1 -maxdepth 1 -not -name "C" -exec rm -rf {} +

%files
%{_bindir}/evolution
%{_libdir}/evolution/
%{_libexecdir}/evolution/
%{_datadir}/evolution/
%{_datadir}/applications/org.gnome.Evolution*.desktop
%{_datadir}/icons/hicolor/*/apps/org.gnome.Evolution*
%{_datadir}/icons/hicolor/*/apps/evolution*
%{_datadir}/glib-2.0/schemas/org.gnome.evolution*
%{_mandir}/man1/evolution.1*
%{_datadir}/GConf/
%{_datadir}/help/C/evolution/
%{_datadir}/locale/*/LC_MESSAGES/
%{_datadir}/metainfo/org.gnome.Evolution*


%files -n evolution-data-server
# Background daemon factories
%{_libexecdir}/evolution-addressbook-factory*
%{_libexecdir}/evolution-calendar-factory*
%{_libexecdir}/evolution-source-registry*
%{_libexecdir}/evolution-user-prompter*
%{_libexecdir}/camel-*

# Core dynamic link libraries
%{_libdir}/libcamel-1.2.so.*
%{_libdir}/libebackend-1.2.so.*
%{_libdir}/libebook-1.2.so.*
%{_libdir}/libebook-contacts-1.2.so.*
%{_libdir}/libecal-2.0.so.*
%{_libdir}/libedata-book-1.2.so.*
%{_libdir}/libedata-cal-2.0.so.*
%{_libdir}/libedataserver-1.2.so.*
%{_libdir}/libedataserverui-1.2.so.*
%{_libdir}/libedataserverui4-1.0.so.*

# Module and architecture-specific directories
%{_libdir}/evolution-data-server/
%{_libexecdir}/evolution-data-server/

# Shared data configurations and service definitions
%{_datadir}/evolution-data-server/
%{_userunitdir}/evolution-*.service
%{_datadir}/dbus-1/services/org.gnome.evolution.dataserver.*
%{_datadir}/glib-2.0/schemas/org.gnome.Evolution.DefaultSources.gschema.xml
%{_sysconfdir}/xdg/autostart/org.gnome.Evolution-alarm-notify.desktop
%{_datadir}/applications/org.gnome.evolution-data-server.*
%{_datadir}/GConf/gsettings/evolution-data-server.convert
%{_datadir}/pixmaps/evolution-data-server/

%files -n evolution-ews
%{_libdir}/evolution-ews/
%{_libdir}/evolution-data-server/addressbook-backends/libebookbackendews.so
%{_libdir}/evolution-data-server/calendar-backends/libecalbackendews.so
%{_libdir}/evolution-data-server/registry-modules/module-ews-backend.so
%{_libdir}/evolution-data-server/registry-modules/module-microsoft365-backend.so
%{_libdir}/evolution/modules/module-ews-configuration.so
%{_libdir}/evolution/modules/module-microsoft365-configuration.so

%files devel
%{_includedir}/evolution-data-server/
%{_includedir}/evolution/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
%autochangelog
