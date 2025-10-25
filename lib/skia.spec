### https://copr-dist-git.fedorainfracloud.org/packages/fed500/skia/skia.git/tree/skia.spec


%global debug_package %{nil}

Name:           skia
# https://chromiumdash.appspot.com/schedule
Version:        129
Release:        1%{?dist}
Summary:        Rendering library

License:        BSD-3-Clause
URL:            https://skia.org
Source0:        https://skia.googlesource.com/skia/+archive/refs/heads/chrome/m%{version}.tar.gz

BuildRequires:  abseil-cpp
BuildRequires:  brotli-devel
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  expat-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glibc-devel
BuildRequires:  gn
BuildRequires:  graphite2-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  highway-devel
BuildRequires:  icu
BuildRequires:  libicu-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libjxl-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libpng-devel
BuildRequires:  libyuv-devel
BuildRequires:  libwebp-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  procps-ng-devel
BuildRequires:  spirv-tools-devel
BuildRequires:  ninja-build
# vulkan - something needs to provide
# vk_mem_alloc.h w
# Need to package
# https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator
#BuildRequires:  vulkan-headers
#BuildRequires:  vulkan-loader-devel
#BuildRequires:  vulkan-tools
#BuildRequires:  vulkan-validation-layers-devel
#BuildRequires:  zlib-ng-compat
#BuildRequires:  zlib-ng-compat-devel

%description
Two dimensional graphics engine

%package devel
Summary:        Skia development files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development header files and libraries for skia graphics engine.

%prep
%setup -c -n %{name}-%{version}


%build

# Enable system Zlib to be used. Bug noted at:
# https://git.savannah.gnu.org/cgit/guix.git/tree/gnu/packages/graphics.scm#n2148
#sed -i 's|deps = \[ "//third_party/zlib" \]|deps = \[\]|g' BUILD.gn
# This is checked before the GN build flags are set, and results in an error if
# it has not been donwloaded, even if it is not used
sed -i 's|deps += \[ "//third_party/externals/spirv[\-]tools:spvtools_val" \]|deps += \[\]|g' BUILD.gn
# dng_sdk is not packaged
# wuffs is not packaged
# ganesh fails to build, maybe try another commit
GN_DEFINES_MAIN=" cc=\"${CC}\""
GN_DEFINES_MAIN+=" cxx=\"${CXX}\""
# Parsing Fedora build flags is problematic
#GN_DEFINES_MAIN+=" extra_cflags=[\"${CFLAGS}\"]"
#GN_DEFINES_MAIN+=" extra_ldflags=[\"${LDFLAGS}\"]"
GN_DEFINES_MAIN+=" is_official_build=true"
GN_DEFINES_MAIN+=" is_component_build=true"
GN_DEFINES_MAIN+=" is_debug=false"
GN_DEFINES_MAIN+=" skia_use_dng_sdk=false"
GN_DEFINES_MAIN+=" skia_use_icu=true"
GN_DEFINES_MAIN+=" skia_use_wuffs=false"
GN_DEFINES_MAIN+=" skia_use_zlib=false"
GN_DEFINES_MAIN+=" skia_enable_gpu=true"
GN_DEFINES_MAIN+=" skia_enable_ganesh=true"
GN_DEFINES_MAIN+=" skia_enable_graphite=true"
GN_DEFINES_MAIN+=" skia_enable_pdf=true"
GN_DEFINES_MAIN+=" skia_enable_spirv_validation=false"
GN_DEFINES_MAIN+=" skia_compile_sksl_tests=false"
GN_DEFINES_MAIN+=" skia_use_system_expat=true"
GN_DEFINES_MAIN+=" skia_use_system_freetype2=true"
GN_DEFINES_MAIN+=" skia_use_system_harfbuzz=true"
GN_DEFINES_MAIN+=" skia_use_system_icu=true"
GN_DEFINES_MAIN+=" skia_use_system_libjpeg_turbo=true"
GN_DEFINES_MAIN+=" skia_use_system_libpng=true"
GN_DEFINES_MAIN+=" skia_use_system_libwebp=true"
#GN_DEFINES_MAIN+=" skia_use_system_zlib=true"
GN_DEFINES_MAIN+=" skia_use_vulkan=false"
# Main build
gn gen out/Build --args="${GN_DEFINES_MAIN}"

# Builds
ninja -C ./out/Build
ls out/Build

%install
mkdir -p %{buildroot}/%{_libdir}
install -m644 out/Build/*.so* %{buildroot}/%{_libdir}/

mkdir -p %{buildroot}/%{_includedir}/skia
find include out/Build -type f -and -\( -name "*.h" -\) -exec install -v -D -m644 {} %{buildroot}%{_includedir}/skia/{} \;

mkdir -p %{buildroot}/%{_libdir}/pkgconfig

cat << EOF > skia.pc
prefix=%{_prefix}
exec_prefix=%{prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: %{summary}
URL: %{url}
Version: %{version}
Libs: -L%{_libdir} -lskia
Cflags: -I%{_includedir}/%{name}
EOF

install -m 644 skia.pc %{buildroot}/%{_libdir}/pkgconfig/

%check
#need a build with tests

%files
%license LICENSE
%doc README
%{_libdir}/libbentleyottmann.so
%{_libdir}/libskia.so
%{_libdir}/libskparagraph.so
%{_libdir}/libskshaper.so
%{_libdir}/libskunicode_core.so
%{_libdir}/libskunicode_icu.so

%files devel
%{_includedir}/skia/
%{_libdir}/pkgconfig/skia.pc

%changelog
%autochangelog