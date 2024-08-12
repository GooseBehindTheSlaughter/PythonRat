# Python Remote Access Trojan

This is a simple RAT made entirely in python, this allowes for running remote commands such as CMD commands as if you were running them on the computer itself.
NOTE this is currently empty and basic asf so dont be suprised if nothing works as expected

## Commands
Shell [COMMAND] - This runs the target command as if you were on the computer itself.
- Example "shell ipconfig"

screenshare - Shares the screen of the client aswell as audio, press Q on the window to close it
stopscreenshare - Stops sharing the screen but usually isnt needed as closing the screenshare window usually handles this

pwd - Prints the current directory the script is running from

cd .. - Changes directory to one folder back

# Planned commands

cd /FOLDER - cds into the targeted folder
ls - Lists all files/folders in the current directory
upload FILE - uploads the file to the client
download FILE downloads the file from the client
run FILE - runs the file 

#### More coming soon.

# Usage
- Firstly download the script and run the requirements.txt to install dependencies
```sh
pip install -r requirements.txt
```

- Then configure config.py to set the target IP and ports (make sure you portforward the ports if youre planning on using across network)

- Next (optional) Compile the client by running (MAKE SURE YOU HAVE PYINSTALLER INSTALLED)
```
compile_client.bat
```

- Then run the server and client and it should connect
