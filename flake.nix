{
  description = "Python development environment with Poetry";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            poetry
          ];

          shellHook = ''
            echo "Python development environment with Poetry is ready!"
            echo "Python, pip, and Poetry are available in your environment."
          '';
        };
      }
    );
} 