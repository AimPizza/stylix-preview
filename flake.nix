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
        python = pkgs.python312;
        pyPkgs = python.pkgs;
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
        stylix-preview = pyPkgs.buildPythonApplication {
          pname = "stylix-preview";
          version = "0.1.0";
          pyproject = true;

          src = ./.;

          propagatedBuildInputs = with pyPkgs; [
            textual
            pyperclip
            pyyaml
          ];

          nativeBuildInputs = with pyPkgs; [
            setuptools
            wheel
          ];

          # no tests rn
          doCheck = false;

          meta = with pkgs.lib; {
            description = "A Textual app to inspect Stylix palettes.";
            license = licenses.mit; # change if different
            mainProgram = "stylix-preview";
            platforms = platforms.linux;
          };
        };

      in
      {
        packages.default = stylix-preview;
        apps.default = {
          type = "app";
          program = "${stylix-preview}/bin/stylix-preview";
        };
        devShell = fhs.env;
      }
    );
}
