Name:           rustdesk
Version:        1.4.3
Release:        1%{?dist}
Summary:        Remote desktop software

License:        GPLv3
URL:            https://github.com/rustdesk/rustdesk
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}-0.x86_64.rpm

ExclusiveArch:  x86_64
BuildRequires: chrpath

%description
RuskDesk is a remote desktop software that allows you to access and control computers remotely.
This spec simply repackages the RPM (prebuilt binary) for distribution via Copr.

%prep
# Nothing to do

%build
# Nothing to do

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

### Strip invalid RPATHs from all ELF binaries (shared objects and executables)
find %{buildroot} -type f \( -name '*.so' -o -perm -111 \) -exec sh -c '
    for bin; do
        if file "$bin" | grep -q ELF && chrpath -l "$bin" 2>/dev/null | grep -q "/workspace/"; then
            chrpath -d "$bin"
        fi
    done
' sh {} +

## The .desktop file is not in `applications` directory (not found in applications menu)
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{buildroot}%{_datadir}/rustdesk/files/rustdesk.desktop %{buildroot}%{_datadir}/applications/rustdesk.desktop

## The executable file rustdesk is not in the PATH, e.g., /usr/bin (not in %{_bindir})
mkdir -p %{buildroot}%{_bindir}
ln -s %{_datadir}/rustdesk/rustdesk %{buildroot}%{_bindir}/rustdesk

## Move the service file to the correct systemd location
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 %{buildroot}%{_datadir}/rustdesk/files/rustdesk.service %{buildroot}/usr/lib/systemd/system/rustdesk.service

%files
%{_bindir}/rustdesk
%{_datadir}/rustdesk/**
%{_datadir}/applications/rustdesk.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.svg
/usr/lib/systemd/system/rustdesk.service

%preun
if [ $1 -eq 0 ]; then
    # Only remove service if this is the last uninstall
    systemctl --no-reload disable rustdesk.service >/dev/null 2>&1 || true
    systemctl --no-reload stop rustdesk.service >/dev/null 2>&1 || true
fi

%changelog
%autochangelog
