### ref: https://github.com/gitbutlerapp/gitbutler/blob/master/.github/workflows/publish.yaml
### The GitButler desktop app is a Tauri-based application
### Revise by Gemini

Name:           gitbutler
Version:        0.20.0
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
### Enforce host environment presence at runtime
Requires:       git-core libgit2 libssh2 openssl-libs

%global debug_package %{nil}

%description
GitButler is a modern Git-based version control interface with both a GUI and CLI built from the ground up for AI-powered workflows.

%prep
%autosetup -n gitbutler-release-%{version}

%build
export CARGO_HOME=./.cargo
export RUSTFLAGS="-C link-arg=-fuse-ld=lld -A unused-imports -A unused-variables"

### FORCE CARGO CRATES TO LINK TO SYSTEM LIBRARIES (UNVENDOR ALL)
export OPENSSL_NO_VENDOR=1
export LIBGIT2_NO_VENDOR=1
export LIBSSH2_SYS_USE_PKG_CONFIG=1
export ZLIB_NO_VENDOR=1

# Leverage sccache if available in the environment
if [ -x "%{_bindir}/sccache" ]; then
    export RUSTC_WRAPPER=%{_bindir}/sccache
fi

# Set up local pnpm binary cache instead of relying on global corepack
mkdir -p .node_modules_local
npm install --prefix .node_modules_local pnpm
export PATH="$(pwd)/.node_modules_local/node_modules/.bin:$PATH"

# Install UI assets
pnpm install --frozen-lockfile

# Explicitly build the background companion engine binaries
cargo build --release --bin but --bin gitbutler-git-askpass

# Compile the UI shell assets matching upstream production flags
pnpm tauri build --no-bundle --features builtin-but,disable-auto-updates

### check build output
find . -type f

%install
### Pull the UI wrapper from the Tauri release target directory
install -Dpm755 target/tauri/release/gitbutler-tauri %{buildroot}%{_bindir}/gitbutler

### Pull the core companion engines from the workspace native release directory
install -Dpm755 target/release/but %{buildroot}%{_bindir}/but
install -Dpm755 target/release/gitbutler-git-askpass %{buildroot}%{_bindir}/gitbutler-git-askpass

### Create desktop file
cat > gitbutler.desktop <<'EOF'
[Desktop Entry]
Name=GitButler
GenericName=Git Client
Comment=Modern Git-based version control interface
Exec=env GDK_BACKEND=x11 WEBKIT_DISABLE_DMABUF_SANDBOX=1 gitbutler %U
Icon=gitbutler
Type=Application
StartupNotify=true
Categories=Utility;Development;RevisionControl;
MimeType=x-scheme-handler/gitbutler;
Keywords=git;gitbutler;version-control;
StartupWMClass=gitbutler-tauri
EOF
install -Dpm644 gitbutler.desktop %{buildroot}%{_datadir}/applications/gitbutler.desktop

### Install Icon
install -Dpm644 crates/gitbutler-tauri/icons/release/128x128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/gitbutler.png

%files
%license LICENSE.md
%{_bindir}/gitbutler
%{_bindir}/but
%{_bindir}/gitbutler-git-askpass
%{_datadir}/applications/gitbutler.desktop
%{_datadir}/icons/hicolor/128x128/apps/gitbutler.png

%changelog
%autochangelog
