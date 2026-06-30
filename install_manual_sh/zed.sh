#!/bin/bash
set -e

#####ANCHOR Info
# This script to update the versions of .spec files in the current directory.

#####ANCHOR Parameters
zed_version=0.214.5-pre  #  0.214.5-pre   0.213.7


install_dir=$HOME/app/zed
mkdir -p $install_dir

#####ANCHOR Download and install
rundir=$(pwd)
mkdir -p tmp_source && cd tmp_source

echo -e "\nTASK: Install Zed version $zed_version to $install_dir\n"

tarfile="zed-linux-x86_64.tar.gz"
if [ ! -f "$tarfile" ]; then
    curl -L -o "$tarfile" "https://github.com/zed-industries/zed/releases/download/v${zed_version}/zed-linux-x86_64.tar.gz"
fi
tar -xzf "$tarfile" -C "$install_dir"

### Create file `zotero.desktop`
if [[ "$zed_version" == *"-pre" ]]; then
    zed_root=$install_dir/zed-preview.app
    WMString="dev.zed.Zed-Preview"
else
    zed_root=$install_dir/zed.app
    WMString="dev.zed.Zed"
fi

zed_bin="$zed_root/bin/zed"

tee $zed_root/share/applications/zed_thang.desktop << EOF
[Desktop Entry]
Name=Zed
GenericName=Text Editor
Exec=$zed_bin %U
Icon=$zed_root/share/icons/hicolor/512x512/apps/zed.png
Type=Application
StartupNotify=true
Categories=Utility;TextEditor;Development;IDE;
MimeType=text/plain;application/x-zerosize;x-scheme-handler/zed;inode/directory;
Actions=NewWorkspace;
Keywords=zed;
StartupWMClass=$WMString

[Desktop Action NewWorkspace]
Name=Open a new workspace
Exec=$zed_bin --new %U
EOF

### Add to the application menu
sudo rm -f /usr/share/applications/zed.desktop || true
sudo ln -s $zed_root/share/applications/zed_thang.desktop /usr/share/applications/zed.desktop

#####ANCHOR Cleanup
cd $rundir
rm -rf tmp_source
echo -e "\n Done"