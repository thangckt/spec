### REF: https://tug.org/texlive/

Name:           texlive-basic
Version:        2026
Release:        1%{?dist}
Summary:        TeX Live distribution

License:        GPLv2+
URL:            https://tug.org/texlive/
#ource0:        http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
#ource0:        https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2026/install-tl-unx.tar.gz
Source0:        https://texlive.info/historic/systems/texlive/%{version}/install-tl-unx.tar.gz


BuildRequires:  tar perl-devel
Requires:       perl perl-YAML-Tiny wget curl

AutoReqProv:    no

%global         install_dir  %{_libexecdir}/texlive/%{version}
%global         debug_package %{nil}

%description
This package automates the installation of a comprehensive TeX system from upstream mirrors directly during system installation.

%prep
%setup -q -c -n texlive_installer

%build
# Nothing to build

%install
### Disable the RPATH QA check (avoid using: chrpath, patchelf)
export QA_RPATHS=$((0x0001|0x0002|0x0004|0x0008|0x0010|0x0020))

### Create a directory to store the installer files on the system temporarily
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a install-tl-*/* %{buildroot}%{_datadir}/%{name}/

### Create wrapper for tlmgr to override system /usr/sbin/tlmgr when use sudo
### Note: We install the wrapper in /usr/local/bin to avoid conflicts with any existing system tlmgr in /usr/sbin, and to ensure it takes precedence in the PATH when using sudo.
mkdir -p %{buildroot}/usr/local/bin
cat > %{buildroot}/usr/local/bin/tlmgr <<EOF
#!/bin/sh
exec %{install_dir}/bin/x86_64-linux/tlmgr "\$@"
EOF
chmod +x %{buildroot}/usr/local/bin/tlmgr

### Set Texlive PATH, export environment variables (PATH, MANPATH, etc.)
mkdir -p %{buildroot}/etc/profile.d
cat > %{buildroot}/etc/profile.d/texlive.sh <<EOF
export PATH=%{install_dir}/bin/x86_64-linux:\$PATH
export MANPATH=%{install_dir}/texmf-dist/doc/man:\$MANPATH
export INFOPATH=%{install_dir}/texmf-dist/doc/info:\$INFOPATH
EOF

### To ensure non-login shells also get the PATH
mkdir -p %{buildroot}/etc/bashrc.d
cat > %{buildroot}/etc/bashrc.d/texlive.sh <<EOF
if [ -f /etc/profile.d/texlive.sh ]; then
  . /etc/profile.d/texlive.sh
fi
EOF

%files
# We only track the wrapper, profiles, and the minimal installer scripts
%{_datadir}/%{name}
/usr/local/bin/tlmgr
/etc/profile.d/texlive.sh
/etc/bashrc.d/texlive.sh

%post
### Explicitly redirecting directly to the controlling terminal /dev/tty
# ensures it bypasses the DNF block buffer entirely and prints *instantly*.
if [ -c /dev/tty ]; then
    exec 3>&1        # Save original stdout to fd 3
    exec 1>/dev/tty  # Redirect stdout to the terminal directly
fi

echo "======================================================="
echo "Starting upstream TeX Live installation streaming..."
echo "This downloads several gigabytes of data and will take time."
echo "======================================================="

### Create the profile template to be used by the installer in %post
cat > /tmp/texlive.profile <<EOF
selected_scheme scheme-basic
TEXDIR          %{install_dir}
TEXMFLOCAL      %{install_dir}/texmf-local
TEXMFSYSVAR     %{install_dir}/texmf-var
TEXMFSYSCONFIG  %{install_dir}/texmf-config
binary_x86_64-linux 1
option_doc 0
option_src 0
EOF

### Run the installer out of the packaged data directory directly to the system destination
# We use 'stdbuf -oL' to force line-buffering on the install-tl Perl engine
stdbuf -oL -eL %{_datadir}/%{name}/install-tl \
    -profile /tmp/texlive.profile \
    -no-interaction \
    -gui text

### Clean up the temporary profile immediately
rm -f /tmp/texlive.profile

### Fix ambiguous and legacy python2 shebangs on the freshly streamed files
find %{install_dir} -type f -exec sed -i \
  -e '1s|^#! */usr/bin/python2$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/env python2$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/python -O$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/python$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/env python$|#!/usr/bin/python3|' \
  {} +

### Clean up internal installation logs
find %{install_dir} -type f \( -name 'install-tl.log' -o -name 'texlive.profile' \) -delete || :

### Fix broken biber (update its versions)
PATH=%{install_dir}/bin/x86_64-linux:$PATH \
    %{install_dir}/bin/x86_64-linux/tlmgr install --reinstall biber

echo "======================================================="
echo "TeX Live installation complete!"
echo "======================================================="

### Restore original stdout if we hijacked it for /dev/tty
if [ -c /dev/tty ]; then
    exec 1>&3 3>&-
fi

%preun
### Since RPM didn't install the streamed files, we must manually purge them on uninstall
if [ $1 -eq 0 ]; then
    rm -rf %{install_dir}
fi

%changelog
%autochangelog