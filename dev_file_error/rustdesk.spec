### REF: https://bugs.mageia.org/attachment.cgi?id=14993
# https://rustdesk.com/docs/en/dev/build/linux/

Name:           rustdesk
Version:        1.4.1
Release:        1%{?dist}
Summary:        Remote desktop software

License:        GPLv3
URL:            https://github.com/rustdesk/rustdesk
# Source0:        %{url}/archive/refs/tags/%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  cargo rust gcc-c++ clang cmake pkgconfig
BuildRequires:  nasm yasm git wget pam-devel

BuildRequires:  libvpx-devel libxdo-devel libyuv-devel
BuildRequires:  pulseaudio opus-devel python3-magnumclient
BuildRequires:  libX11-devel libxcb-devel xorg-x11-proto-devel
BuildRequires:  wayland-devel wayland-protocols-devel
BuildRequires:  libXrandr-devel libXfixes-devel libXinerama-devel

BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

# Needed for .desktop + icon install
BuildRequires:  desktop-file-utils

%global debug_package %{nil}

%description
RuskDesk is a remote desktop software that allows you to access and control computers remotely.

%prep
# Clone source
git clone --recurse-submodules https://github.com/rustdesk/rustdesk.git rustdesk
cd rustdesk
git checkout %{version}
git submodule update --init --recursive
cargo generate-lockfile

## Finalize, move source code to top-level directory
cd ..
cp -a rustdesk/. ./
rm -rf rustdesk

%build
export CARGO_HOME="${PWD}/.cargo"
export MAGNUM_OPUS_SYSTEM=1
export VCPKG_ROOT=""
export PKG_CONFIG_ALLOW_CROSS=1
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/share/pkgconfig
export RUST_BACKTRACE=full
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_DEBUG=true
export RUSTFLAGS="-C link-arg=-Wl,-rpath,/usr/lib"

export OPUS_NO_PKG_CONFIG=1
export OPUS_INCLUDE_DIR=/usr/include
export OPUS_LIB_DIR=/usr/lib64

# Fetch dependencies, but don’t build yet (to allow patching)
cargo fetch --locked

# Patch mkvparser.cc (add missing include)
mkvparser_file=$(find "$CARGO_HOME" -type f -name 'mkvparser.cc' 2>/dev/null | head -n1)
if [ -n "$mkvparser_file" ]; then
    echo "ANCHOR: Patching mkvparser.cc"
    sed -i '1i#include <cstdint>' "$mkvparser_file" || true
fi

# Build with system libraries feature to avoid vcpkg usage if supported
cargo build --release --verbose

%install
install -Dm755 target/release/rustdesk %{buildroot}%{_bindir}/rustdesk

## Desktop entry
install -Dm644 res/rustdesk.desktop %{buildroot}%{_datadir}/applications/rustdesk.desktop

## Icons
install -Dm644 res/128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/rustdesk.png
install -Dm644 res/scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/rustdesk.svg

## systemd service file
install -Dm644 res/rustdesk.service %{buildroot}%{_unitdir}/rustdesk.service

%files
%license LICENSE
%{_bindir}/rustdesk
%{_datadir}/applications/rustdesk.desktop
%{_datadir}/icons/hicolor/*/apps/rustdesk.*
%{_unitdir}/rustdesk.service

%changelog
%autochangelog