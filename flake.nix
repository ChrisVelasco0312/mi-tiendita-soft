{
  description = "Python development environment with Poetry and LSP plugins";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
        python-with-lsp = python.withPackages (ps: with ps; [
          # LSP server and plugins
          python-lsp-server
          pylsp-mypy
          python-lsp-ruff
          python-lsp-black
          pyls-isort
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python-with-lsp
            pkgs.poetry
            pkgs.python312Packages.textual
            pkgs.python312Packages.textual-dev
            pkgs.python312Packages.pandas
            pkgs.python312Packages.openpyxl
            pkgs.python312Packages.pandas-stubs
          ];

          shellHook = ''
            echo "🐍 Python dev environment ready with Poetry and LSP plugins!"
            echo "Tools: python, pip, poetry, pylsp, ruff, mypy, black, isort"

            if [ "$AUTO_NVIM" = "1" ]; then
              nvim .
            fi

            if [ "$START" = "1" ]; then
	            poetry run python main.py
            fi
            
          '';
        };
      }
    );
}

