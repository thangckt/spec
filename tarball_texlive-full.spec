### REF: https://tug.org/texlive/
### https://www.tug.org/historic/
### This spec version apply hybrid approach
## Step 1: Install only `tlmgr` and the installer scripts in the RPM, which are very small (a few MB).
## Step 2: In the %post section. use `tlmgr` to stream the full TeX Live installation. This way, we get the latest packages and avoid bloating the RPM with a large tarball.


Name:           texlive-full
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
Obsoletes:      texlive-basic <= 2025

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

### STAGE 1: Install just the core infrastructure inside %{buildroot}
### Create the profile template to install a minimal infrastructure-only environment
cat > minimal_infra.profile <<EOF
selected_scheme scheme-infraonly
TEXDIR          %{buildroot}%{install_dir}
TEXMFLOCAL      %{buildroot}%{install_dir}/texmf-local
TEXMFSYSVAR     %{buildroot}%{install_dir}/texmf-var
TEXMFSYSCONFIG  %{buildroot}%{install_dir}/texmf-config
binary_x86_64-linux 1
option_doc 0
option_src 0
EOF

### Run the installer. the scheme-infraonly is incredibly light (~15MB of internal files).
./install-tl-*/install-tl -profile minimal_infra.profile -no-interaction -gui text

### Clean up the temporary local profile file
rm -f minimal_infra.profile

### --- FIX: SANITIZE BUILDROOT PATH LEAKAGE ---
### Strip out the temporary %{buildroot} prefix from all internal config, text, and database files
find %{buildroot}%{install_dir} -type f -exec sed -i "s|%{buildroot}||g" {} +

### Also ensure there are no lingering backup files created by sed (if any)
find %{buildroot}%{install_dir} -type f -name "*~" -delete || :
### -------------------------------------------

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
%{install_dir}
/usr/local/bin/tlmgr
/etc/profile.d/texlive.sh
/etc/bashrc.d/texlive.sh

%post
### Explicitly redirecting directly to the controlling terminal /dev/tty
log_message() {
    if [ -c /dev/tty ]; then echo "$1" >/dev/tty; else echo "$1"; fi
}

### STAGE 2: Use the pre-installed `tlmgr` to stream the full TeX Live installation directly from upstream mirrors.
log_message "======================================================="
log_message " Starting TeX Live full installation streaming"
log_message " This may take time, please be patient..."
log_message "======================================================="
    PATH=%{install_dir}/bin/x86_64-linux:$PATH
    stdbuf -oL -eL %{install_dir}/bin/x86_64-linux/tlmgr install scheme-full



### Fix broken biber (update its versions)
PATH=%{install_dir}/bin/x86_64-linux:$PATH \
    %{install_dir}/bin/x86_64-linux/tlmgr install --reinstall biber

%preun
### Since RPM didn't install the streamed files, we must manually purge them on uninstall
if [ $1 -eq 0 ]; then
    echo "Purging TeX Live application directory..."
    rm -rf %{install_dir}
fi

%changelog
%autochangelog