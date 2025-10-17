#!/bin/bash

#####ANCHOR Info
# This script to update the versions of .spec files in the current directory.

#####ANCHOR Parameters
### Helper functions
fetch_gitlab_version() {
    # There are 2 types of GitLab repositories:
    # 1. https://gitlab.com/username/repo -> use tags: (/api/v4/projects/:id/repository/tags)
    # 2. https://gitlab.com/namespace/project -> use releases (/api/v4/projects/:id/releases)

    # Extract base domain and project path
    local base_url project_path
    base_url=$(echo "$repo_url" | sed -E 's|^(https://[^/]+).*|\1|')
    project_path=$(echo "$repo_url" | sed -E 's|https://[^/]+/||; s|/-/.*||')
    local project_path_encoded
    project_path_encoded=$(echo "$project_path" | sed 's|/|%2F|g')
    local base_api_url="${base_url}/api/v4/projects/${project_path_encoded}"

    local new_version=""
    local tmp_versions=$(mktemp)

    # Try releases API first
    curl -s "${base_api_url}/releases?per_page=100" |
        grep -oP '"tag_name":"v?\K[0-9]+(\.[0-9]+)*' >>"$tmp_versions"

    # Then try tags if releases empty or missing
    curl -s "${base_api_url}/repository/tags?per_page=100" |
        grep -oP '"name":"v?\K[0-9]+(\.[0-9]+)*' >>"$tmp_versions"

    new_version=$(sort -V "$tmp_versions" | tail -n1)
    rm -f "$tmp_versions"

    if [[ -z "$new_version" ]]; then
        echo "Failed to get version for $repo_url" >&2
        return 1
    fi

    echo "$new_version"
}

function fetch_github_version() {
    local repo_url="$1"
    local new_version
    new_version=$(curl -sL "${repo_url}/releases/latest" \
        | sed -nE 's|.*href="[^"]*/tag/v?([0-9]+(\.[0-9]+)+)".*|\1|p' \
        | head -n1)
    if [[ -z "$new_version" ]]; then
        echo "Failed to get version for $repo_url" >&2
        exit 1
    fi
    echo "$new_version"
}

fetch_zotero_version() {
    # '-D -': prints headers to stdout.'
    local url="https://www.zotero.org/download/client/dl?channel=release&platform=linux-x86_64"
    local final_url new_version

    # Fetch only headers (-I), follow redirects (-L), and extract the last Location header
    final_url=$(curl -Ls -o /dev/null -D - "$url" | grep -i '^location:' | tail -n1 | awk '{print $2}' | tr -d '\r')

    new_version=$(echo "$final_url" | sed -nE 's|.*/release/([0-9.]+)/.*|\1|p')
    if [[ -z "$new_version" ]]; then
        echo "Failed to extract Zotero version from redirect" >&2
        return 1
    fi
    echo "$new_version"
}

function update_spec_version() {
    local spec_file="$1"
    local new_version="$2"
    local store_file="$3"

    current_version=$(grep -E '^Version:' "$spec_file" | awk '{print $2}')
    # Compare versions using sort -V (version sort)
    if [[ "$new_version" != "$current_version" ]] && [[ "$(printf "%s\n%s" "$current_version" "$new_version" | sort -V | tail -n1)" == "$new_version" ]]; then
        sed -i "s/^Version:[[:space:]]\+$current_version/Version:        $new_version/" "$spec_file"
        tee >$store_file <<<"$spec_file"
    else
        new_version=""
    fi
    printf "%-15s %-15s %s\n" "$current_version" "$new_version" "$spec_file"
}

#####SECTION: From GitHub
printf "%-15s %-15s %s\n" "Old_ver" "New_ver" "File"
printf "%-15s %-15s %s\n" "---------" "---------" "---------"

### initialize store file
store_file="changed_specs.txt"
[ -f "$store_file" ] && rm -f "$store_file"

#####ANCHOR rustdesk
repo_url="https://github.com/rustdesk/rustdesk"
spec_files="repackRPM_rustdesk.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR electerm
repo_url="https://github.com/electerm/electerm"
spec_files="repackRPM_electerm.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR github-desktop
repo_url="https://github.com/pol-rivero/github-desktop-plus"
spec_files="repackRPM_github-desktop-plus.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR OnlyOffice
repo_url="https://github.com/ONLYOFFICE/DesktopEditors"
spec_files="repackRPM_onlyoffice.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR goldendict
repo_url="https://github.com/goldendict/goldendict"
spec_files="goldendict.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR rssguard
repo_url="https://github.com/martinrotter/rssguard"
spec_files="rssguard.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR zed
repo_url="https://github.com/zed-industries/zed"
spec_files="zed.spec"
new_version=$(fetch_github_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR Ovito
repo_url="https://gitlab.com/stuko/ovito"
spec_files="ovito.spec"
new_version=$(fetch_gitlab_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR Evolution
repo_url="https://gitlab.gnome.org/GNOME/evolution-data-server"
spec_files="evolution1-data-server.spec"
new_version=$(fetch_gitlab_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

repo_url="https://gitlab.gnome.org/GNOME/evolution"
spec_files="evolution2.spec"
new_version=$(fetch_gitlab_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

repo_url="https://gitlab.gnome.org/GNOME/evolution-ews"
spec_files="evolution3-ews.spec"
new_version=$(fetch_gitlab_version "$repo_url")
update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR Zotero
spec_files="tarball_zotero.spec"
new_version=$(fetch_zotero_version)
update_spec_version "$spec_files" "$new_version" "$store_file"
#####!SECTION


#####SECTION: Retired
#####ANCHOR FreeFileSync
# repo_url="https://gitlab.com/opensource-tracking/FreeFileSync"
# spec_files="tarball_freefilesync.spec"
# new_version=$(fetch_gitlab_version "$repo_url")
# update_spec_version "$spec_files" "$new_version" "$store_file"

#####ANCHOR pdf4qt
# repo_url="https://github.com/JakubMelka/PDF4QT"
# spec_files="pdf4qt.spec"
# new_version=$(fetch_github_version "$repo_url")
# update_spec_version "$spec_files" "$new_version" "$store_file"


#####ANCHOR vscodium
# repo_url="https://github.com/VSCodium/vscodium"
# spec_files="codium.spec"
# new_version=$(fetch_github_version "$repo_url")
# update_spec_version "$spec_files" "$new_version" "$store_file"