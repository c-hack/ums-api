{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    shellHook = ''
              source "$(pipenv --venv)/bin/activate"
              export FLASK_APP=ums_api
              export FLASK_DEBUG=1  # to enable autoreload
              export MODE=debug

              flask create_db
    '';
}

