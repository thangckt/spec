### ref: https://github.com/gitbutlerapp/gitbutler/blob/master/.github/workflows/publish.yaml
### Revise by Gemini

Name:           gitbutler
Version:        0.19.13
Release:        1%{?dist}
Summary:        Modern Git-based version control interface

License:        FSL-1.1-MIT
URL:            https://github.com/gitbutlerapp/gitbutler
Source0:        %{url}/archive/refs/tags/release/%{version}.tar.gz


BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gcc gcc-c++ clang cmake git-core lld sccache

### Linux Tauri and system dependencies specified in DEVELOPMENT.md
BuildRequires:  nodejs >= 20, npm
BuildRequires:  webkit2gtk4.1-devel libxdo-devel openssl-devel libayatana-appindicator3-devel
BuildRequires:  librsvg2-devel alsa-lib-devel perl-devel fontconfig-devel wayland-devel libxkbcommon-x11-devel

%description
GitButler is a modern Git-based version control interface with both a GUI and CLI built from the ground up for AI-powered workflows.

%prep
%autosetup -n gitbutler-release-%{version}

%build
export CARGO_HOME=./.cargo
export RUSTFLAGS="-C link-arg=-fuse-ld=lld"

# Leverage sccache if available in the environment
if [ -x "%{_bindir}/sccache" ]; then
    export RUSTC_WRAPPER=%{_bindir}/sccache
fi

# Bypass global corepack constraint by installing pnpm into the build environment
mkdir -p .node_modules_local
npm install --prefix .node_modules_local pnpm
export PATH="$(pwd)/.node_modules_local/node_modules/.bin:$PATH"

# Install Node.js frontend dependencies
pnpm install --frozen-lockfile

# Build supplementary binaries and core CLI engine ('but')
cargo build --release --bin but --bin gitbutler-git-askpass

# Build the production release using Tauri
pnpm tauri build --features devtools,builtin-but,disable-auto-updates --config crates/gitbutler-tauri/tauri.conf.nightly-local.json

%install
# Install the main tauri desktop binary wrapper
install -Dpm755 target/release/gitbutler-tauri %{buildroot}%{_bindir}/gitbutler

# Install the accompanying core 'but' CLI utility binary
install -Dpm755 target/release/but %{buildroot}%{_bindir}/but
install -Dpm755 target/release/gitbutler-git-askpass %{buildroot}%{_bindir}/gitbutler-git-askpass

## Desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/gitbutler.desktop <<'EOF'
[Desktop Entry]
Name=GitButler
GenericName=Git Client
Comment=Modern Git-based version control interface
Exec=gitbutler %U
Icon=gitbutler
Type=Application
StartupNotify=true
Categories=Utility;Development;RevisionControl;
MimeType=x-scheme-handler/gitbutler;
Keywords=git;gitbutler;version-control;
StartupWMClass=gitbutler-tauri
EOF

### App Icon (Tauri populates icons in the src-tauri/icons directory during setup)
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
