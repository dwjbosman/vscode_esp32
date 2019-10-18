# Introduction

This repo shows how to work with Micropython on an ESP32 device, while using Microsoft VSCode. It makes use of the VSCode remote container extension. The extension connects to a Docker container in which all the ESP32 tooling has been installed. The tooling has been compiled from source.

# Tooling

In the Docker image the following tools have been installed:

    1. xtensa-esp32 toolchain (compiled from source!)
    2. esp-idf (freetos ESP32 library)    
    3. micropython
    4. esptool (allows to erase flash)
    5. mpfshell (allows to put files on the ESP32 flash, start the REPL)
    6. micropy-cli (allows the setup micropython projects including intellisense and pylinting)



# Tutorial

    1. Install VSCode and Docker
    2. Install the remote docker extension in VSCode
    3. Go into the .devcontainer folder of this repo
    3. Run make pull_hub to get the EPS32 tooling image from Docker hub, or run make image to locally build the docker image containing the tooling (this will take quite a long time!)
    4. First plugin the ESP32 device (otherwise /dev/ttyUSB won't be available in the container).
    5. Go into the .devcontainer folder of this repo and run ./ex_bash (this creates the container and mounts your home dir inside the container)
    6. Add the following to: ~/.config/Code/User/globalStorage/ms-vscode-remote.remote-containers/imageConfigs/planetbosman%2fesp32_vscode.json <BR>
<BR>
    Note replace workspacefolder path to the path of the example project in this repo.
<BR>
<pre>
{
    "execArgs": [
        "-u", "vscode"
    ],

    "extensions": [
        "ms-python.python",
        "junhuanchen.mpfshell"
    ],
    "workspaceFolder": "/home/dinne/vscode/esp32/example_project"
}
</pre>


    8. In vscode choode ctrl-shift+P: Attach to running container
    9. Ctrl+Shit+P: Run the command "Python: Select interpreter (python 3), select python Linter
    11. Use esptool to erase flash

<pre>
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
</pre>

    12. To flash the micropython firmware open a VScode terminal and: i

<pre>
cd /root/micropython/ports/esp32 && sudo make deploy
</pre>

    13. open folder "example_project". Open a terminal and upload various files

<pre>
mpfs -n --nohelp -c "open ttyUSB0; put ssd1306.py; put main.py;"
</pre>

    14. Reset the device

<pre>
esptool.py --chip esp32 --port /dev/ttyUSB0 --after hard_reset chip_id
</pre>

    14. Start a REPL (the REPL can be quit with CTRL+]) 

<pre>
mpfs -n --nohelp -c "open ttyUSB0; r;"
</pre>

# TODO
    
    Will be adding instructions to add custom C libaries 




