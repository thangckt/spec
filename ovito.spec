### REF: https://www.ovito.org/docs/current/development/build_linux.html

Name:           ovito
Version:        3.15.0
Release:        1%{?dist}
Summary:        OVITO - Open Visualization Tool (GUI)

License:        MIT
URL:            https://gitlab.com/stuko/ovito
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:        %{url}/-/raw/master/doc/manual/images/team/ovito_logo_128.png
# zstd is a git submodule not included in the GitLab archive tarball
Source2:        https://github.com/facebook/zstd/archive/refs/tags/v1.5.7.tar.gz#/zstd-v1.5.7.tar.gz

BuildRequires:  cmake ninja-build gcc-c++ pkg-config
BuildRequires:  qt6-qtbase-devel qt6-qtsvg-devel
BuildRequires:  boost-devel netcdf-devel libssh-devel ffmpeg-free-devel libzstd-devel
BuildRequires:  python3-sphinx python3-sphinx_rtd_theme python3-devel
BuildRequires:  pkgconfig(libzstd)

Requires:       qt6-qtbase qt6-qtsvg boost netcdf libssh

%description
OVITO is a scientific data visualization and analysis software for atomistic, molecular and other particle-based simulations.

%prep
%autosetup -n %{name}-v%{version}
# Populate the zstd git submodule (not included in the archive tarball)
mkdir -p src/3rdparty/zstd
tar -xzf %{SOURCE2} --strip-components=1 -C src/3rdparty/zstd

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_DO_STRIP=ON
## add '--target documentation' to build the documentation (may error and heavy size)
%cmake_build

%install
%cmake_install
strip %{buildroot}%{_bindir}/ovito

# Install .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=OVITO
GenericName=Scientific Visualization Tool
Exec=ovito
Icon=ovito
Type=Application
Terminal=false
Categories=Science;Education;Graphics;
EOF

# Copy icon (since it is not included in the source)
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/ovito.png

# Clean up
rm -f %{buildroot}%{_bindir}/ssh_askpass

%files
%{_bindir}/ovito
%{_datadir}/ovito/
%{_datadir}/applications/ovito.desktop
%{_datadir}/icons/hicolor/scalable/apps/ovito.png
%{_prefix}/lib/ovito/

%changelog
%autochangelog