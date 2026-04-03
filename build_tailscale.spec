### https://gitlab.com/shadowblue/allthetools/
### Revise by Claude

%global debug_package %{nil}

Name:           tailscale
Version:        1.96.5
Release:        1%{?dist}
Summary:        The easiest, most secure way to use WireGuard and 2FA.

License:        BSD-3-Clause
URL:            https://github.com/tailscale/tailscale
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  systemd-rpm-macros git-core go

%description
The easiest, most secure way to use WireGuard and 2FA.

%prep
%autosetup -n %{name}-%{version}

%build
export LDFLAGS="-X tailscale.com/version.longStamp=%{version} -X tailscale.com/version.shortStamp=%{version}"

# Build tailscale CLI & tailscaled daemon
go build -ldflags "-w ${LDFLAGS}" -o %{name} ./cmd/%{name}
go build -ldflags "-w ${LDFLAGS}" -o tailscaled ./cmd/tailscaled

# Generate shell completions
mkdir -p generated_completions
./%{name} completion bash > generated_completions/%{name}
./%{name} completion fish > generated_completions/%{name}.fish
./%{name} completion zsh  > generated_completions/_%{name}

%install
# Install CLI binary
install -Dpm 0755 ./%{name} %{buildroot}%{_bindir}/%{name}
# Install daemon binary
install -Dpm 0755 ./tailscaled %{buildroot}%{_bindir}/tailscaled

# Install shell completions
install -Dpm 0644 generated_completions/%{name}      -t %{buildroot}/%{bash_completions_dir}/
install -Dpm 0644 generated_completions/%{name}.fish -t %{buildroot}/%{fish_completions_dir}/
install -Dpm 0644 generated_completions/_%{name}     -t %{buildroot}/%{zsh_completions_dir}/

# Create systemd service and install
mkdir -p %{buildroot}%{_unitdir}
cat > %{buildroot}%{_unitdir}/tailscaled.service << 'EOF'
[Unit]
Description=Tailscale node agent
Documentation=https://tailscale.com/kb/
Wants=network-pre.target
After=network-pre.target NetworkManager.service systemd-resolved.service

[Service]
# Port for incoming VPN packets; remote nodes are automatically informed
Environment="PORT=41641"
ExecStart=/usr/bin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock --port=${PORT}
ExecStopPost=/usr/bin/tailscaled --cleanup

Restart=on-failure
RuntimeDirectory=tailscale
RuntimeDirectoryMode=0755
StateDirectory=tailscale
StateDirectoryMode=0700
CacheDirectory=tailscale
CacheDirectoryMode=0750
Type=notify

[Install]
WantedBy=multi-user.target
EOF

%post
### reloads systemd's daemon configuration to recognize the new service file
%systemd_post tailscaled.service
### automatically enable and start tailscaled on install
systemctl enable tailscaled.service
systemctl start tailscaled.service

%preun
### Stops the running service
systemctl stop tailscaled.service 2>/dev/null || true
### disables the service and removes it from startup
%systemd_preun tailscaled.service

%postun
### performs final cleanup (mean for upgrade scenarios)
%systemd_postun_with_restart tailscaled.service

%files
%license LICENSE
%doc README.md
### Binaries
%{_bindir}/%{name}
%{_bindir}/tailscaled
### Systemd service
%{_unitdir}/tailscaled.service
### Shell completions
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%changelog
%autochangelog
