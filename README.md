# Docker container for ESP32 and micropython development

    1. Go into the .devcontainer folder
    2. make image
    3. wait :)
    4. After the image is built. Run ./ex_bash
    5. start VSCode
    6. Attach to running container
    7. Install extensions: serial_monitor, ms-python.python, pymakr, micropy-cli

## TODO
    Currently step 7 has to be done manually. Also ex_bash creates the correct user in the container and mounts the the home folder. An alias user called 'vscode'. By running commands as this user you ensure that the correct permissions are used. However I have not found a way yet to automatically run 'su' when attaching to the container. So in the VSCode terminal you still have to run "su vscode".



