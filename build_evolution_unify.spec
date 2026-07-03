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
# Define a safe staging root that RPM won't automatically delete
STAGING_ROOT="%{_builddir}/stage_root"
rm -rf "$STAGING_ROOT"
mkdir -p "$STAGING_ROOT"

### Keep compiler environment safe and standard
export PKG_CONFIG_PATH="$STAGING_ROOT%{_libdir}/pkgconfig:$STAGING_ROOT%{_datadir}/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="$STAGING_ROOT%{_libdir}:$LD_LIBRARY_PATH"

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
DESTDIR="$STAGING_ROOT" %cmake_install
cd ..

### Snapshot of what EDS installed (Paths stored relative to system root)
find "$STAGING_ROOT" -type f | sed "s|^$STAGING_ROOT||" | sort > %{_builddir}/eds_files.txt

### Relocate prefix inside EDS files so Evolution can resolve them locally
find "$STAGING_ROOT" -type f \( -name "*.pc" -o -name "*.cmake" \) -exec sed -i "s|%{_prefix}|$STAGING_ROOT%{_prefix}|g" {} +


################ANCHOR 2. Build Evolution
cd evolution-%{version}
%cmake \
    -DCMAKE_PREFIX_PATH="$STAGING_ROOT%{_prefix}" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath-link,$STAGING_ROOT%{_libdir} -Wl,-rpath-link,$STAGING_ROOT%{_libdir}/evolution-data-server" \
    -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath-link,$STAGING_ROOT%{_libdir} -Wl,-rpath-link,$STAGING_ROOT%{_libdir}/evolution-data-server" \
    -DENABLE_PLUGINS=all \
    -DENABLE_MAINTAINER_MODE=OFF \
    -DENABLE_GTK_DOC=OFF \
    -DENABLE_MARKDOWN=OFF
%cmake_build
DESTDIR="$STAGING_ROOT" %cmake_install
cd ..

### Files added since the EDS snapshot = Evolution's own files
find "$STAGING_ROOT" -type f | sed "s|^$STAGING_ROOT||" | sort > %{_builddir}/after_evolution.txt
comm -13 %{_builddir}/eds_files.txt %{_builddir}/after_evolution.txt > %{_builddir}/evolution_files.txt

### Redirect paths inside Evolution's development targets without double-prepending EDS files
while read -r file; do
    if [[ "$file" == *.pc || "$file" == *.cmake ]]; then
        sed -i "s|%{_prefix}|$STAGING_ROOT%{_prefix}|g" "$STAGING_ROOT$file"
    fi
done < %{_builddir}/evolution_files.txt


################ANCHOR 3. Build Evolution EWS
cd evolution-ews-%{version}
%cmake \
    -DCMAKE_PREFIX_PATH="$STAGING_ROOT%{_prefix}" \
    -DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=ON \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,-rpath-link,$STAGING_ROOT%{_libdir} -Wl,-rpath-link,$STAGING_ROOT%{_libdir}/evolution-data-server" \
    -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-rpath-link,$STAGING_ROOT%{_libdir} -Wl,-rpath-link,$STAGING_ROOT%{_libdir}/evolution-data-server"
%cmake_build
DESTDIR="$STAGING_ROOT" %cmake_install
cd ..

### Files added since the Evolution snapshot = EWS's own files
find "$STAGING_ROOT" -type f | sed "s|^$STAGING_ROOT||" | sort > %{_builddir}/after_ews.txt
comm -13 %{_builddir}/after_evolution.txt %{_builddir}/after_ews.txt > %{_builddir}/ews_files.txt

### CLEANUP: Revert staging paths back to clean production targets (/usr) before moving to packaging
find "$STAGING_ROOT" -type f \( -name "*.pc" -o -name "*.cmake" \) -exec sed -i "s|$STAGING_ROOT%{_prefix}|%{_prefix}|g" {} +


%install
# 1. RPM just ran 'rm -rf %{buildroot}' right before this block.
# 2. Recreate the buildroot base safely:
mkdir -p %{buildroot}

# 3. Cleanly clone our entire post-processed staging tree over into the official package root
cp -a %{_builddir}/stage_root/* %{buildroot}/


%files -f evolution_files.txt

%files -n evolution-data-server -f eds_files.txt

%files -n evolution-ews -f ews_files.txt

%changelog
%autochangelog
