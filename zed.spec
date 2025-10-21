### ref: https://github.com/terrapkg/packages/blob/frawhide/anda/devs/zed/stable/zed.spec
### Note:
#  - simplify desktop file from the original: https://github.com/zed-industries/zed/blob/main/crates/zed/resources/zed.desktop.in

Name:           zed
Version:        0.208.6
Release:        1%{?dist}
Summary:        High-performance, multiplayer code editor

License:        AGPL-3.0-only AND Apache-2.0 AND GPL-3.0-or-later
URL:            https://zed.dev/
Source0:        https://github.com/zed-industries/zed/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gcc, gcc-c++, clang, cmake, git, lld, sccache
BuildRequires:  alsa-lib-devel, fontconfig-devel, wayland-devel
BuildRequires:  libxkbcommon-x11-devel, openssl-devel
BuildRequires:  libzstd-devel, vulkan-loader-devel, libcurl-devel
BuildRequires:  expat-devel, libxcb-devel, libX11-devel, libXi-devel

Conflicts:      zed-nightly
Conflicts:      zed-preview

# disable shebang mangling entirely (common for Rust packages)
%global __brp_mangle_shebangs %{nil}

%description
Code at the speed of thought — Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.

%prep
%autosetup -n zed-%{version}

### Or replace all pre section by clone Zed with submodules
# git clone --recurse-submodules https://github.com/zed-industries/zed.git zed
# cd zed
# git checkout v%{version}
# git submodule update --init --recursive
# cd ..
# cp -a zed/. ./
# rm -rf zed

%build
export CARGO_HOME=.cargo

# Use lld linker (much faster than bfd/gold)
export RUSTFLAGS="-C link-arg=-fuse-ld=lld"

# Enable compiler cache (helps if persistent_buildroot is on)
export RUSTC_WRAPPER=%{_bindir}/sccache

# Build only the main binary, not tests/examples
cargo build -j$(nproc) --release --bin zed

%install
install -Dpm755 target/release/zed %{buildroot}%{_bindir}/zed

## Desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/zed.desktop <<'EOF'
[Desktop Entry]
Name=Zed Editor
GenericName=Text Editor
Exec=zed %U
Icon=zed
Type=Application
StartupNotify=true
Categories=Utility;TextEditor;Development;IDE;
MimeType=text/plain;application/x-zerosize;x-scheme-handler/zed;
Actions=NewWorkspace;
Keywords=zed;
StartupWMClass=dev.zed.Zed

[Desktop Action NewWorkspace]
Name=Open a new workspace
Exec=zed --new %U
EOF

## Icon
install -Dpm644 crates/zed/resources/app-icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/zed.png

%files
%license LICENSE-AGPL LICENSE-APACHE LICENSE-GPL
%{_bindir}/zed
%{_datadir}/applications/zed.desktop
%{_datadir}/icons/hicolor/128x128/apps/zed.png

%changelog
%autochangelog
