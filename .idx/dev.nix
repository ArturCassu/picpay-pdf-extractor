{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = [ pkgs.python3 pkgs.pkg-config pkgs.mysql ];
  idx = {
    workspace = {
      onCreate = {
        default.openFiles = [ "README.md" "app/main.py" ];
      };
      onStart = { run-server = "./devserver.sh"; };
    };
  };
}