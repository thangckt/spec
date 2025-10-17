### REF: https://github.com/lfnovo/open-notebook?tab=readme-ov-file#%EF%B8%8F-full-installation

Name:           open-notebook
Version:        0.3.2
Release:        1%{?dist}
Summary:        Open Notebook - A privacy-focused alternative to Google's Notebook LM

License:        MIT
URL:            https://github.com/lfnovo/open-notebook
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc make autoconf automake libtool
BuildRequires:  python3

%description
Open Notebook is an open source, privacy-focused alternative to Google's Notebook LM. Why give Google more of our data when we can take control of our own research workflows?

%prep
%autosetup -n %{name}-%{version}

%build
# Setup isolated Python environment
python3 -m venv buildenv
source buildenv/bin/activate
pip install --upgrade pip
# Install Python dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Autotools build
%autoreconf -vfi
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}

%install
source buildenv/bin/activate
make install DESTDIR=%{buildroot}

# Include auxiliary scripts or helpers if present
if [ -d scripts ]; then
    install -Dm0755 scripts/* %{buildroot}%{_bindir}/
fi

# Validate install integrity
find %{buildroot} -type f -o -type l

%files


%changelog
%autochangelog