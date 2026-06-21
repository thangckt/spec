### REF: https://src.fedoraproject.org/rpms/freerdp/blob/rawhide/f/freerdp.spec
## https://download.copr.fedorainfracloud.org/results/ifas/freerdp/epel-10-x86_64/10591219-freerdp/freerdp.spec

# Can be rebuilt with FFmpeg support enabled by passing
# "--with=ffmpeg" to mock/rpmbuild; or by globally
# setting these variables:
# https://bugzilla.redhat.com/show_bug.cgi?id=2242028
#global _with_ffmpeg 1

# Can be rebuilt with OpenCL support enabled by passing # "--with=opencl"
# or by globally setting:
#global _opencl 1

# Force uwac to be static to avoid conflicts with freerdp2
# %global _with_static_uwac 1

# Disable unwanted dependencies for RHEL
%{!?rhel:%global _with_aom 1}
%{!?rhel:%global _with_openh264 1}
%{!?rhel:%global _with_sdl_client 1}
%{!?rhel:%global _with_soxr 1}
%if 0%{?fedora} || 0%{?rhel} > 10
%global _with_uriparser 1
%endif

# Disable support for AAD WebView popup since it uses webkit2gtk-4.0
#global _with_webview 1

Name:           freerdp
Epoch:          2
Version:        3.27.1
Release:        2%{?dist}
Summary:        Free implementation of the Remote Desktop Protocol (RDP)

# The effective license is Apache-2.0 but:
# client/SDL/dialogs/font/* is OFL-1.1
# uwac/libuwac/* is HPND
# uwac/protocols/server-decoration.xml is LGPL-2.1-or-later
# winpr/libwinpr/ncrypt/pkcs11-headers/pkcs11.h is LicenseRef-Fedora-Public-Domain
License:        Apache-2.0 AND HPND AND LGPL-2.1-or-later AND LicenseRef-Fedora-Public-Domain AND OFL-1.1
URL:            http://www.freerdp.com/

# The license of the winpr/libwinpr/crt/unicode_builtin.c file is not allowed.
# See: https://gitlab.com/fedora/legal/fedora-license-data/-/issues/498
# Run the ./freerdp_download_and_repack.sh script to prepare tarball.
Source0:        https://github.com/FreeRDP/FreeRDP/releases/download/%{version}/freerdp-%{version}.tar.gz
# ource1:        freerdp_download_and_repack.sh

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 3.13
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
BuildRequires:  lame-devel
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  turbojpeg-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXv-devel
%{?_with_opencl:BuildRequires: opencl-headers >= 3.0}
%{?_with_opencl:BuildRequires: ocl-icd-devel}
%{?_with_openh264:BuildRequires:  pkgconfig(openh264)}
%{?_with_x264:BuildRequires:  x264-devel}
BuildRequires:  pam-devel
BuildRequires:  xmlto
BuildRequires:  zlib-devel
%{!?rhel:BuildRequires:  multilib-rpm-config}

BuildRequires:  cmake(json-c)
# Packaging error led to cmake files in the wrong place
# Fixed in https://src.fedoraproject.org/rpms/uriparser/c/1b07302bfc80983fbf84283783370e8338d36429
%{?_with_uriparser:BuildRequires:  (cmake(uriparser) and uriparser-devel)}

%{?_with_aom:BuildRequires:  pkgconfig(aom)}
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(fdk-aac)
BuildRequires:  pkgconfig(fuse3)
BuildRequires:  pkgconfig(libcbor)
BuildRequires:  pkgconfig(libfido2)
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libwebp)
%{?_with_aom:BuildRequires:  pkgconfig(libyuv)}
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
%{?_with_sdl_client:BuildRequires:  cmake(SDL3)}
%{?_with_sdl_client:BuildRequires:  cmake(SDL3_image)}
%{?_with_sdl_client:BuildRequires:  cmake(SDL3_ttf)}
%{?_with_soxr:BuildRequires:  pkgconfig(soxr)}
BuildRequires:  pkgconfig(sso-mib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
%{?_with_webview:BuildRequires:  pkgconfig(webkit2gtk-4.0)}
BuildRequires:  pkgconfig(xkbcommon)

%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec) >= 57.48.101
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
}

Provides:       xfreerdp = %{?epoch}:%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}

%description
The xfreerdp & wlfreerdp Remote Desktop Protocol (RDP) clients from the FreeRDP
project.

xfreerdp & wlfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%package        libs
Summary:        Core libraries implementing the RDP protocol
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-plugins < 1:1.1.0
Provides:       %{name}-plugins = %{?epoch}:%{version}-%{release}
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 3.13

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}-libs.

%package        server
Summary:        Server support for %{name}
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}

%description    server
The %{name}-server package contains servers which can export a desktop via
the RDP protocol.

%package -n     libwinpr
Summary:        Windows Portable Runtime
Provides:       %{name}-libwinpr = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-libwinpr < 1:1.2.0

%description -n libwinpr
WinPR provides API compatibility for applications targeting non-Windows
environments. When on Windows, the original native API is being used instead of
the equivalent WinPR implementation, without having to modify the code using it.

%package -n     libwinpr-devel
Summary:        Windows Portable Runtime development files
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 3.13

%description -n libwinpr-devel
The %{name}-libwinpr-devel package contains libraries and header files for
developing applications that use %{name}-libwinpr.

%prep
%autosetup -p1 -n freerdp-%{version}

# Rpmlint fixes
find . -name "*.h" -exec chmod 664 {} \;
find . -name "*.c" -exec chmod 664 {} \;

%conf
%cmake \
    -DBUILD_TESTING=ON \
    -DBUILD_TESTING_NO_H264=ON \
    -DCHANNEL_RDP2TCP=ON \
    -DCHANNEL_RDP2TCP_CLIENT=ON \
    -DCHANNEL_RDPEWA=ON \
    -DCHANNEL_RDPEWA_CLIENT=ON \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
    -DWITH_ALSA=ON \
    -DWITH_AAD=ON \
    -DWITH_CAIRO=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON \
    -DWITH_CLIENT=ON \
    -DWITH_CLIENT_SDL=%{?_with_sdl_client:ON}%{?!_with_sdl_client:OFF} \
    -DWITH_SDL_IMAGE_DIALOGS=%{?_with_sdl_client:ON}%{?!_with_sdl_client:OFF} \
    -DWITH_DSP_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_FDK_AAC=ON \
    -DWITH_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_FUSE=ON \
    -DWITH_GSM=ON \
    -DWITH_GFX_AV1=%{?_with_aom:ON}%{?!_with_aom:OFF} \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_JSONC_REQUIRED=ON \
    -DWITH_KEYBOARD_LAYOUT_FROM_FILE=ON \
    -DWITH_KRB5=ON \
    -DWITH_LAME=ON \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENCL=%{?_with_opencl:ON}%{?!_with_opencl:OFF} \
    -DWITH_OPENH264=%{?_with_openh264:ON}%{?!_with_openh264:OFF} \
    -DWITH_OPENSSL=ON \
    -DWITH_OPUS=ON \
    -DWITH_PCSC=ON \
    -DWITH_PKCS11=ON \
    -DWITH_PULSE=ON \
    -DWITH_RDTK=ON \
    -DWITH_SAMPLE=OFF \
    -DWITH_SERVER=ON \
    -DWITH_SERVER_INTERFACE=ON \
    -DWITH_SHADOW_X11=ON \
    -DWITH_SHADOW_MAC=ON \
    -DWITH_SOXR=%{?_with_soxr:ON}%{?!_with_soxr:OFF} \
    -DWITH_SSO_MIB=ON \
    -DWITH_SWSCALE=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_TIMEZONE_COMPILED=OFF \
    -DWITH_TIMEZONE_FROM_FILE=ON \
    -DWITH_URIPARSER=%{?_with_uriparser:ON}%{?!_with_uriparser:OFF} \
    -DWITH_VERBOSE_WINPR_ASSERT=OFF \
    -DWITH_VIDEO_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_WAYLAND=ON \
    -DWITH_WEBVIEW=%{?_with_webview:ON}%{?!_with_webview:OFF} \
    -DWITH_X11=ON \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XI=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XRENDER=ON \
    -DWITH_XTEST=ON \
    -DWITH_XV=ON \
    -DWITH_ZLIB=ON \
%ifarch x86_64
    -DWITH_SSE2=ON \
    -DWITH_VAAPI=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
%else
    -DWITH_SSE2=OFF \
%endif
%ifarch armv7hl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=OFF \
%endif
%ifarch armv7hnl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=ON \
%endif
%ifarch armv5tel armv6l armv7l
    -DARM_FP_ABI=soft \
    -DWITH_NEON=OFF \
%endif
    -DUWAC_FORCE_STATIC_BUILD=%{?_with_static_uwac:ON}%{?!_with_static_uwac:OFF} \
    -DWINPR_UTILS_IMAGE_PNG=ON \
    -DWINPR_UTILS_IMAGE_WEBP=ON \
    -DWINPR_UTILS_IMAGE_JPEG=ON \
    %{nil}

%build
%cmake_build
%check
export CTEST_OUTPUT_ON_FAILURE=1
%cmake_build --target test

%install
%cmake_install
find %{buildroot} -name "*.a" -delete

%if %{undefined rhel}
%multilib_fix_c_header --file %{_includedir}/freerdp3/freerdp/build-config.h
%endif

%files
%{?_with_sdl_client:
%{_bindir}/sdl-freerdp
}
%{_bindir}/winpr-hash
%{_bindir}/winpr-makecert
%{_bindir}/wlfreerdp
%{_bindir}/xfreerdp
%{?_with_sdl_client:
%{_mandir}/man1/sdl-freerdp.1*
}
%{_mandir}/man1/winpr-hash.1*
%{_mandir}/man1/winpr-makecert.1*
%{_mandir}/man1/wlfreerdp.1*
%{_mandir}/man1/xfreerdp.1*

%files libs
%license LICENSE
%doc README.md ChangeLog
%{_datadir}/FreeRDP/
%{_libdir}/freerdp3/
%{_libdir}/libfreerdp-client3.so.*
%{_libdir}/libfreerdp-server3.so.*
%{_libdir}/libfreerdp-server-proxy3.so.*
%{_libdir}/libfreerdp-shadow3.so.*
%{_libdir}/libfreerdp-shadow-subsystem3.so.*
%{_libdir}/libfreerdp3.so.*
%{?!_with_static_uwac:
%{_libdir}/libuwac0.so.*
}
%{_libdir}/librdtk0.so.*
%{_mandir}/man7/wlog.*

%files devel
%{_includedir}/freerdp3/
%{?!_with_static_uwac:
%{_includedir}/uwac0/
}
%{_includedir}/rdtk0/
%{_libdir}/cmake/FreeRDP3/
%{_libdir}/cmake/FreeRDP-Client3/
%{_libdir}/cmake/FreeRDP-Proxy3/
%{_libdir}/cmake/FreeRDP-Server3/
%{_libdir}/cmake/FreeRDP-Shadow3/
%{?!_with_static_uwac:
%{_libdir}/cmake/uwac0/
}
%{_libdir}/cmake/rdtk0/
%{_libdir}/libfreerdp-client3.so
%{_libdir}/libfreerdp-server3.so
%{_libdir}/libfreerdp-server-proxy3.so
%{_libdir}/libfreerdp-shadow3.so
%{_libdir}/libfreerdp-shadow-subsystem3.so
%{_libdir}/libfreerdp3.so
%{?!_with_static_uwac:
%{_libdir}/libuwac0.so
}
%{_libdir}/librdtk0.so
%{_libdir}/pkgconfig/freerdp3.pc
%{_libdir}/pkgconfig/freerdp-client3.pc
%{_libdir}/pkgconfig/freerdp-server3.pc
%{_libdir}/pkgconfig/freerdp-server-proxy3.pc
%{_libdir}/pkgconfig/freerdp-shadow3.pc
%{?!_with_static_uwac:
%{_libdir}/pkgconfig/uwac0.pc
}
%{_libdir}/pkgconfig/rdtk0.pc

%files server
%{_bindir}/freerdp-proxy
%{_bindir}/freerdp-shadow-cli
%{_mandir}/man1/freerdp-proxy.1*
%{_mandir}/man1/freerdp-shadow-cli.1*

%files -n libwinpr
%license LICENSE
%doc README.md ChangeLog
%{_datadir}/WinPR/
%{_libdir}/libwinpr3.so.*
%{_libdir}/libwinpr-tools3.so.*

%files -n libwinpr-devel
%{_libdir}/cmake/WinPR3/
%{_libdir}/cmake/WinPR-tools3/
%{_includedir}/winpr3/
%{_libdir}/libwinpr3.so
%{_libdir}/libwinpr-tools3.so
%{_libdir}/pkgconfig/winpr3.pc
%{_libdir}/pkgconfig/winpr-tools3.pc

%changelog
%autochangelog
