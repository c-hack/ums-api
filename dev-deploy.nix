{ pkgs ? import <nixpkgs> {} }:
let
    nur = import (builtins.fetchTarball "https://github.com/nix-community/NUR/archive/master.tar.gz") {
      inherit pkgs;
    };
    myPython = (with pkgs; nur.repos.neumantm.pythonWithPipenv.override { myPythonDerivation = python37; myPythonPackages = pp: with pp; [ pylint ]; });
in 
  pkgs.mkShell {
    buildInputs = with pkgs; [myPython];
    shellHook = ''
              function initPipenvIfNeeded {
                if ! pipenv --venv > /dev/null 2>&1 ;then
                  pipenv install --dev  
                fi
              }              

              function loadPipenv {
                export loadPipenvDepth=$(expr $loadPipenvDepth + 1) 
                initPipenvIfNeeded
                source "$(pipenv --venv)/bin/activate"
                if ! python -c "" ;then
                  if [ $loadPipenvDepth -gt 3 ] ;then
                    echo "Could not load pipenv after 3 tries."
                    exit 1
                  fi
                  pipenv --rm
                  loadPipenv
                fi
              } 

              loadPipenv || exit
              unset loadPipenvDepth

              export FLASK_APP=ums_api
              export FLASK_DEBUG=1  # to enable autoreload
              export MODE=debug

              flask create_db
    '';
  }

