### ref: https://github.com/gitbutlerapp/gitbutler/blob/master/.github/workflows/publish.yaml
### The GitButler desktop app is a Tauri-based application
### Revise by Gemini

Name:           gitbutler
Version:        0.20.1
Release:        1%{?dist}
Summary:        Modern Git-based version control interface

License:        FSL-1.1-MIT
URL:            https://github.com/gitbutlerapp/gitbutler
Source0:        %{url}/archive/refs/tags/release/%{version}.tar.gz

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
GitButler is a modern Git-based version control interface with both a GUI and CLI built from the ground up for AI-powered workflows.

%prep
%autosetup -n gitbutler-release-%{version}

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
cargo build --release --bin but --bin gitbutler-git-askpass

# Compile the UI shell assets matching upstream production flags
export TAURI_ENV_DEBUG=false
pnpm tauri build --no-bundle --features builtin-but,disable-auto-updates

### check build output
# find . -type f

%install
### Install core components into system binaries
install -Dpm755 target/tauri/release/gitbutler-tauri %{buildroot}%{_bindir}/gitbutler-tauri
install -Dpm755 target/release/but %{buildroot}%{_bindir}/but
install -Dpm755 target/release/gitbutler-git-askpass %{buildroot}%{_bindir}/gitbutler-git-askpass

### Create wrapper script for main executable
cat > gitbutler_wrapper << 'EOF'
#!/bin/bash
# Fix WebKitGTK rendering crashes on modern Mesa/Fedora systems
export GDK_BACKEND=x11
export WEBKIT_DISABLE_DMABUF_SANDBOX=1
export WEBKIT_DISABLE_COMPOSITING_MODE=1
export WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS=0

exec %{_bindir}/gitbutler-tauri "$@"
EOF
install -Dpm755 gitbutler_wrapper %{buildroot}%{_bindir}/gitbutler

### Create desktop file
cat > gitbutler.desktop <<'EOF'
[Desktop Entry]
Name=GitButler
GenericName=Git Client
Exec=gitbutler %U
Icon=gitbutler
Type=Application
StartupNotify=true
Categories=Utility;Development;RevisionControl;
MimeType=x-scheme-handler/gitbutler;
Keywords=git;gitbutler;version-control;
StartupWMClass=gitbutler-tauri
EOF

desktop-file-validate gitbutler.desktop
install -Dpm644 gitbutler.desktop %{buildroot}%{_datadir}/applications/gitbutler.desktop

### Install Icon
install -Dpm644 crates/gitbutler-tauri/icons/release/128x128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/gitbutler.png

%files
%license LICENSE.md
%{_bindir}/gitbutler
%{_bindir}/gitbutler-tauri
%{_bindir}/but
%{_bindir}/gitbutler-git-askpass
%{_datadir}/applications/gitbutler.desktop
%{_datadir}/icons/hicolor/128x128/apps/gitbutler.png

%changelog
%autochangelog
