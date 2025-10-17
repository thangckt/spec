### Note: must use python3.11 to have distutils. Newer versions of Python may not include distutils.

Name:           electerm
Version:        1.100.46
Release:        1%{?dist}
Summary:        Terminal/SSH/SFTP client (Electron-based)

License:        MIT
URL:            https://github.com/electerm/electerm
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# Node/Electron native build deps
BuildRequires:  nodejs >= 22
BuildRequires:  npm
BuildRequires:  python3
BuildRequires:  make gcc-c++
BuildRequires:  libxkbfile-devel libsecret-devel libnotify-devel

%description
Electerm is a terminal/ssh/telnet/serialport/sftp client

%prep
%autosetup -n electerm-%{version}

%build
# Install all deps, including dev, for full build & packaging
npm ci --unsafe-perm --no-audit --no-fund

# Run vite build (prepares work/app)
npm run vite-build

# Run electron-builder Linux RPM build
npx electron-builder --linux

%install
# Install into /usr/share/electerm
mkdir -p %{buildroot}%{_datadir}/electerm
cp -a work/app/. %{buildroot}%{_datadir}/electerm/
cp -a node_modules %{buildroot}%{_datadir}/electerm/
cp -a package.json %{buildroot}%{_datadir}/electerm/

# Wrapper script
install -Dm755 /dev/stdin %{buildroot}%{_bindir}/electerm <<'EOF'
#!/bin/sh
exec electron %{_datadir}/electerm/app.js "$@"
EOF

# check
ls %{buildroot}%{_bindir}/electerm

%files
%license LICENSE
%doc README.md
%{_bindir}/electerm
%{_datadir}/electerm

%changelog
%autochangelog