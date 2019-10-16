# Docker container for ESP32 and micropython development

    1. Go into the .devcontainer folder
    2. make image
    3. wait :)
    4. First plugin the device (otherwise ttyUSB won't be available in the container).
    5. After the image is built. Run ./ex_bash

    6. Add the following to: ~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/imageConfigs/vscode_esp32_image.json

<pre>
{
    "execArgs": [
        "-u", "vscode"
    ],

    "extensions": [
        "ms-python.python",
        "junhuanchen.mpfshell"
    ],
    "workspaceFolder": "/home//vscode/esp32/example_project"
}
</pre>


    7. start VSCode, install remote container plugin
    8. Attach to running container
    9. Ctrl+Shit+P: Run the command "Python: Select interpreter (python 3), select python Linter
    10. Install plugins: python, mpfshell
    11. Run in a VSCode terminal, micropy init (this installs the stubs)
    12. To flash the micropython firmware: cd micropython && make deploy
    13. via mpfshell you can put files, run commands etc., also check available commands via Ctrl+Shift+P





