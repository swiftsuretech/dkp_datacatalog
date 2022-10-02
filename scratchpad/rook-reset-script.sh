#!/bin/bash

node_shell_install(){
    curl -LO https://github.com/kvaps/kubectl-node-shell/raw/master/kubectl-node_shell
    chmod +x ./kubectl-node_shell
    sudo mv ./kubectl-node_shell /usr/local/bin/kubectl-node_shell
}


if ! command -v kubectl-node_shell &> /dev/null
then
    node_shell_install
    exit
fi

for node in $(kubectl get no -o name); do
    NODE=$(echo $node | awk '{split($0,a,"/"); print a[2]}')
    echo $NODE
    kubectl node-shell $NODE -- ls -alh /var/lib/rook
    kubectl node-shell $NODE -- rm -rf /var/lib/rook
done