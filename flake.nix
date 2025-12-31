{
  description = "pixi env";
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs =
    { flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        fhs = pkgs.buildFHSEnv {
          name = "pixi-env";

          targetPkgs = pkgs: (with pkgs; [ pixi ]);

          extraBwrapArgs = [
            "--bind"
            "/etc/stylix"
            "/etc/stylix"
          ];
        };
      in
      {
        devShell = fhs.env;
      }
    );
}
