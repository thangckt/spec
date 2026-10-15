### ref: https://othmaneblial.github.io/MobaRust/docs.html#source
### Revise by Gemini

Name:           mobarust
Version:        0.1.31
Release:        1%{?dist}
Summary:        MobaXterm alternative built with Rust

License:        FSL-1.1-MIT
URL:            https://github.com/OthmaneBlial/MobaRust
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz


BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gcc gcc-c++ clang cmake git-core lld sccache
### Linux Tauri UI and system layout dependencies specified in DEVELOPMENT.md
BuildRequires:  nodejs >= 20, npm
BuildRequires:  webkit2gtk4.1-devel libxdo-devel libayatana-appindicator3-devel
BuildRequires:  librsvg2-devel alsa-lib-devel fontconfig-devel wayland-devel libxkbcommon-x11-devel
### Fedora system libraries for fully unvendored Rust compilation
BuildRequires:  openssl-devel, libgit2-devel, zlib-devel, libssh2-devel
BuildRequires:  perl-FindBin, perl-File-Compare, perl-podlators
BuildRequires:  xdg-utils
BuildRequires:  desktop-file-utils libglibutil-devel

### Enforce host environment presence at runtime
Requires:       git-core libgit2 libssh2 openssl-libs

%global debug_package %{nil}

%description
Free, open-source MobaXterm alternative built with Rust

%prep
%autosetup -n mobarust-release-%{version}

%build
### Set up isolated Rust environment using official RPM helper structures
export CARGO_HOME=./.cargo
export RUSTFLAGS="-C link-arg=-fuse-ld=lld -A unused-imports -A unused-variables"

### Force Cargo crates to link to system libraries (unvendor all)
export OPENSSL_NO_VENDOR=1
export LIBGIT2_NO_VENDOR=1
export LIBSSH2_SYS_USE_PKG_CONFIG=1
export ZLIB_NO_VENDOR=1

# Leverage sccache if available in the environment
if [ -x "%{_bindir}/sccache" ]; then
    export RUSTC_WRAPPER=%{_bindir}/sccache
fi

# Set up local pnpm environment to isolate the build from global npm states
mkdir -p .node_modules_local
npm install --prefix .node_modules_local pnpm
export PATH="$(pwd)/.node_modules_local/node_modules/.bin:$PATH"
export PNPM_HOME="$(pwd)/.pnpm-store"

# Install UI production assets
pnpm install --frozen-lockfile

# Explicitly build the background companion engine binaries
cargo build --release --bin but --bin mobarust-git-askpass

# Compile the UI shell assets matching upstream production flags
export TAURI_ENV_DEBUG=false
pnpm tauri build --no-bundle --features builtin-but,disable-auto-updates

### check build output
# find . -type f

%install
### Install core components into system binaries
install -Dpm755 target/tauri/release/mobarust-tauri %{buildroot}%{_bindir}/mobarust-tauri
install -Dpm755 target/release/but %{buildroot}%{_bindir}/but
install -Dpm755 target/release/mobarust-git-askpass %{buildroot}%{_bindir}/mobarust-git-askpass

### Create wrapper script for main executable
cat > mobarust_wrapper << 'EOF'
#!/bin/bash
# Fix WebKitGTK rendering crashes on modern Mesa/Fedora systems
export GDK_BACKEND=x11
export WEBKIT_DISABLE_DMABUF_SANDBOX=1
export WEBKIT_DISABLE_COMPOSITING_MODE=1
export WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS=0

exec %{_bindir}/mobarust-tauri "$@"
EOF
install -Dpm755 mobarust_wrapper %{buildroot}%{_bindir}/mobarust

### Create desktop file
cat > mobarust.desktop <<'EOF'
[Desktop Entry]
Name=mobarust
GenericName=Git Client
Exec=mobarust %U
Icon=mobarust
Type=Application
StartupNotify=true
Categories=Utility;Development;RevisionControl;
MimeType=x-scheme-handler/mobarust;
Keywords=git;mobarust;version-control;
StartupWMClass=mobarust-tauri
EOF

desktop-file-validate mobarust.desktop
install -Dpm644 mobarust.desktop %{buildroot}%{_datadir}/applications/mobarust.desktop

### Install Icon
install -Dpm644 crates/mobarust-tauri/icons/release/128x128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/mobarust.png

%files
%license LICENSE.md
%{_bindir}/mobarust
%{_bindir}/mobarust-tauri
%{_bindir}/but
%{_bindir}/mobarust-git-askpass
%{_datadir}/applications/mobarust.desktop
%{_datadir}/icons/hicolor/128x128/apps/mobarust.png

%changelog
%autochangelog
