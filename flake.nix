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
            "--bind"
            "${pkgs.base16-schemes}/share/themes"
            "/etc/schemes/16"
          ];
        };
      in
      {
        devShell = fhs.env;
      }
    );
}
