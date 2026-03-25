#!/bin/bash
# Fake interactive shell for demo recording
# Intercepts /product-build command and runs simulation

printf "\033[32m❯\033[0m "
read -r INPUT

if [[ "$INPUT" == /product-build* ]]; then
    printf "\n"
    bash /Users/charles/product-playbook/demo/build-sim.sh
else
    printf "\n⚠️  unknown command: %s\n" "$INPUT"
fi
