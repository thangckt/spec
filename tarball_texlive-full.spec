### REF: https://tug.org/texlive/
### https://www.tug.org/historic/
### Mirror list: https://ctan.org/mirrors/mirmon
### This spec version apply hybrid approach
## Step 1: Install only `tlmgr` and the installer scripts in the RPM, which are very small (a few MB).
## Step 2: In the %post section. use `tlmgr` to stream the full TeX Live installation. This way, we get the latest packages and avoid bloating the RPM with a large tarball.


Name:           texlive-full
Version:        2026
Release:        1%{?dist}
Summary:        TeX Live distribution

License:        GPLv2+
URL:            https://tug.org/texlive/

Source0:        https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/%{version}/install-tl-unx.tar.gz
#ource0:        https://texlive.info/historic/systems/texlive/%{version}/install-tl-unx.tar.gz
#ource0:        http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz


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
#####ANCHOR STAGE 1: Install just the core infrastructure inside %{buildroot}
### Install texlive to a temporary directory to avoid embedding %{buildroot} in the file-paths
mkdir -p tmp_texlive
tmp_install_dir=$(realpath tmp_texlive)

### Create the profile template to install a minimal infrastructure-only environment
cat > minimal_infra.profile <<EOF
selected_scheme scheme-infraonly
TEXDIR          ${tmp_install_dir}
TEXMFLOCAL      ${tmp_install_dir}/texmf-local
TEXMFSYSVAR     ${tmp_install_dir}/texmf-var
TEXMFSYSCONFIG  ${tmp_install_dir}/texmf-config
binary_x86_64-linux 1
option_doc 0
option_src 0
EOF

### Run the installer. the scheme-infraonly is incredibly light (~15MB of internal files).
./install-tl-*/install-tl -profile minimal_infra.profile -no-interaction -gui text

## Fix ambiguous and legacy python2 shebangs
find ${tmp_install_dir} -type f -exec sed -i \
  -e '1s|^#! */usr/bin/python2$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/env python2$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/python -O$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/python$|#!/usr/bin/python3|' \
  -e '1s|^#! */usr/bin/env python$|#!/usr/bin/python3|' \
  {} +

## Remove unnecessary build files
find ${tmp_install_dir} -type f \( -name 'install-tl.log' -o -name 'texlive.profile' \) -delete || :

## Copy staged install into %{buildroot}
mkdir -p %{buildroot}%{install_dir}
cp -a "$tmp_install_dir"/* %{buildroot}%{install_dir}/


#####ANCHOR Create wrapper for tlmgr to override system /usr/sbin/tlmgr when use sudo
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
# ensures it bypasses the DNF block buffer entirely and prints *instantly*.
if [ -c /dev/tty ]; then
    exec 3>&1        # Save original stdout to fd 3
    exec 1>/dev/tty  # Redirect stdout to the terminal directly
fi

#####ANCHOR STAGE 2: Use the pre-installed `tlmgr` to stream the full TeX Live installation directly from upstream mirrors.
echo ""
echo "======================================================="
echo " Starting TeX Live full installation streaming"
echo " This may take time, please be patient..."
echo "======================================================="
    PATH=%{install_dir}/bin/x86_64-linux:$PATH
    # %{install_dir}/bin/x86_64-linux/tlmgr option repository https://ctan.math.illinois.edu/systems/texlive/tlnet/

    stdbuf -oL -eL %{install_dir}/bin/x86_64-linux/tlmgr update --self
    stdbuf -oL -eL %{install_dir}/bin/x86_64-linux/tlmgr install scheme-full

    ### CRITICAL: Rebuild the filename search databases (ls-R files)
    # This ensures your engines (pdflatex, lualatex, etc.) can discover the newly streamed files
    echo "Rebuilding TeX Live filename databases..."
    %{install_dir}/bin/x86_64-linux/texhash %{install_dir}

### Restore original stdout if we hijacked it for /dev/tty
if [ -c /dev/tty ]; then
    exec 1>&3 3>&-
fi

%preun
### Since RPM didn't install the streamed files, we must manually purge them on uninstall
if [ $1 -eq 0 ]; then
    echo "Purging TeX Live application directory..."
    rm -rf %{install_dir}
fi

%changelog
%autochangelog