{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
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

