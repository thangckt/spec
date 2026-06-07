### The Electron bundled git is a customized git with extra features.
### This spec try to make githubDesktop work with the system git

Name:           github-desktop-plus
Version:        3.5.12.0
Release:        1%{?dist}
Summary:        GitHub Desktop Plus with system git support

License:        MIT
URL:            https://github.com/pol-rivero/github-desktop-plus
Source0:        %{url}/releases/download/v%{version}/GitHubDesktopPlus-v%{version}-linux-x86_64.rpm

Requires:       git

%description
GitHub Desktop Plus is a graphical Git client for managing GitHub repositories easily.
This spec simply repackages the RPM for distribution via Copr.

%prep
# Nothing to build

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

# Define the exact internal paths where GitHub Desktop expects its Git utilities
local_git_bindir="%{buildroot}/usr/lib/%{name}/resources/app/git/bin"
local_git_execdir="%{buildroot}/usr/lib/%{name}/resources/app/git/libexec/git-core"

# 1. Completely clear out the problematic bundled binaries
rm -rf "$local_git_bindir"/*
rm -rf "$local_git_execdir"/*

# 2. Re-create the directories just in case
mkdir -p "$local_git_bindir"
mkdir -p "$local_git_execdir"

# 3. Create symlinks pointing the app's internal calls to your system's native paths
ln -sf %{_bindir}/git "$local_git_bindir"/git
ln -sf %{_libexecdir}/git-core/git-remote-https "$local_git_execdir"/git-remote-https
ln -sf %{_libexecdir}/git-core/git-remote-http  "$local_git_execdir"/git-remote-http

# (Optional) Link any other core utilities the app might call directly
ln -sf %{_bindir}/git "$local_git_execdir"/git

%files
%{_bindir}/%{name}
/usr/lib/%{name}/
%{_datadir}/doc/%{name}/copyright
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
%autochangelog
