### REF: https://github.com/envmodules/modules/blob/main/share/rpm/environment-modules.spec.in

Name:           modules
Version:        5.6.0
Release:        1%{?dist}
Summary:        Environment Modules

License:        GPL-2.0-or-later
URL:            https://github.com/envmodules/modules
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc make autoconf automake libtool
BuildRequires:  tcl-devel procps-ng-devel
BuildRequires:  python3 less

%description
The Environment Modules package provides for the dynamic modification of a user's environment via modulefiles.
Each modulefile contains the information needed to configure the shell for an application.
Modules can be loaded, unloaded, or switched dynamically.

%prep
%autosetup -n %{name}-%{version}

%build
./configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir}
%make_build

%install
%make_install

# Symlink shell init scripts into /etc/profile.d (relative, not absolute)
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
ln -s ../../..%{_prefix}/init/profile.sh %{buildroot}%{_sysconfdir}/profile.d/modules.sh
ln -s ../../..%{_prefix}/init/profile.csh %{buildroot}%{_sysconfdir}/profile.d/modules.csh

# check all files are installed
find %{buildroot} -type f -o -type l

%files
%{_bindir}/modulecmd
%{_bindir}/envml
%{_bindir}/add.modules
%{_bindir}/mkroot

# Libraries and tcl extension
%{_prefix}/libexec/modulecmd.tcl
%{_prefix}/lib/libtclenvmodules.so

# Config installed in /usr/etc (upstream oddity)
%{_prefix}/etc/initrc
%{_prefix}/etc/siteconfig.tcl

# Init scripts and default modulefiles
%{_prefix}/init
%{_prefix}/modulefiles

# Editor support
%{_datadir}/doc
%{_datadir}/vim
%{_datadir}/emacs
%{_datadir}/nagelfar

# Symlink shell init scripts
%config(noreplace) %{_sysconfdir}/profile.d/modules.sh
%config(noreplace) %{_sysconfdir}/profile.d/modules.csh

%changelog
%autochangelog