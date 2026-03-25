#!/bin/zsh
# VHS demo setup: custom prompt + intercept /product-build command

export PS1=$'\033[32m❯\033[0m '

function command_not_found_handler() {
  if [[ "$1" == "/product-build" ]]; then
    bash /Users/charles/product-playbook/demo/build-sim.sh
  else
    printf "zsh: command not found: %s\n" "$1" >&2
    return 127
  fi
}
