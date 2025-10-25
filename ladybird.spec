### https://github.com/LadybirdBrowser/ladybird/blob/master/Documentation/BuildInstructionsLadybird.md

Name:           ladybird
Version:        0.0.1
Release:        1%{?dist}
Summary:        Ladybird — an independent web browser (pre-alpha)

License:        BSD-2-Clause
URL:            https://github.com/LadybirdBrowser/ladybird
Source0:        https://github.com/LadybirdBrowser/ladybird.git

BuildRequires:  cmake >= 3.25
BuildRequires:  ninja-build gcc-c++ pkg-config git
BuildRequires:  autoconf-archive automake ccache liberation-sans-fonts libtool nasm patchelf perl-FindBin perl-IPC-Cmd perl-lib perl-Time-Piece zlib-ng-compat-static
BuildRequires:  libdrm-devel libglvnd-devel qt6-qtbase-devel qt6-qtmultimedia-devel qt6-qttools-devel qt6-qtwayland-devel

BuildRequires:  simdutf-devel fast_float-devel libtommath-devel openssl-devel libsqlite3x-devel libicu-devel fontconfig-devel

%description
Ladybird is an independent web browser implementing a new engine (LibWeb/LibJS).

%prep
#autosetup

### Clone the repository with submodules
git clone --recurse-submodules https://github.com/LadybirdBrowser/ladybird.git ladybird
cd ladybird
# git checkout %{version}
git checkout master
git submodule update --init --recursive

## Move source to expected build directory root
cd ..
cp -a ladybird/. ./
rm -rf ladybird

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_QT=ON -DSKIA_ENABLED=OFF
%cmake_build

%install
%cmake_install
strip %{buildroot}%{_bindir}/ladybird

## Install .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=LadyBird
GenericName=LadyBird Web Browser
Exec=ladybird
Icon=ladybird
Type=Application
Terminal=false
Categories=Internet;WebBrowser;
EOF

## Copy icon (since it is not included in the source)
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.png

%files
%{_bindir}/ladybird
%{_datadir}/ladybird/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.png
%{_prefix}/lib/ladybird/

%changelog
%autochangelog