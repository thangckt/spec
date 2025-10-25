### https://github.com/LadybirdBrowser/ladybird/blob/master/Documentation/BuildInstructionsLadybird.md

Name:           ladybird
Version:        0.1.0
Release:        1%{?dist}
Summary:        A new independent web browser

License:        2-clause BSD license
URL:            https://github.com/LadybirdBrowser/ladybird
#Source0:        %{url}/archive/refs/tags/%{version}.tar.gz
Source0:        https://github.com/LadybirdBrowser/ladybird.git

BuildRequires:  cmake ninja-build gcc-c++ pkg-config
BuildRequires:  autoconf-archive automake ccache curl git libdrm-devel liberation-sans-fonts libglvnd-devel libtool nasm patchelf perl-FindBin perl-IPC-Cmd perl-lib perl-Time-Piece qt6-qtbase-devel qt6-qtmultimedia-devel qt6-qttools-devel qt6-qtwayland-devel tar unzip zip zlib-ng-compat-static

Requires:

%description
LadyBird is a new independent web browser.

%prep
#autosetup

### Clone the repository with submodules
git clone --recurse-submodules https://github.com/LadybirdBrowser/ladybird.git ladybird
cd ladybird
git checkout %{version}
git submodule update --init --recursive

## Move source to expected build directory root
cd ..
cp -a ladybird/. ./
rm -rf ladybird

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_QT=ON
%cmake_build

%install
%cmake_install
strip %{buildroot}%{_bindir}/ladybird

## Install .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=LadyBird
GenericName=Scientific Visualization Tool
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