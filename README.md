# PiFmTx-neo <img src="web/logo.png" width="150" align="left">

![GitHub issues](https://img.shields.io/github/issues/NotHavocc/pifmtx-neo)
![GitHub all releases](https://img.shields.io/github/downloads/NotHavocc/Upifmtx-neo/total)
![GitHub](https://img.shields.io/github/license/NotHavocc/pifmtx-neo)
![Static Badge](https://img.shields.io/badge/open_source-with_%3C3-blue)


A new and improved version of [PiFmTx](https://github.com/NotHavocc/pifmtx), the raspberry pi FM transmitter, with fresh features and a nice looking web-ui. Powered by [Pi-FM-RDS.](https://github.com/christophejacquet/pifmrds)

> [!CAUTION]  
> Legal Notice: PiFmTx-neo is a software tool intended for educational, experimental, and hobbyist purposes only. **Unauthorized FM transmission may violate local, national, or international laws and regulations.** Users are solely responsible for complying with all applicable laws regarding radio frequency use. The developers of PiFmTx-neo do not condone or assume any liability for illegal use, interference with licensed communications, or any damage caused by the software. By using PiFmTx-neo, you acknowledge that you understand the legal responsibilities of transmitting over FM frequencies and agree to use this software only in a lawful manner.

## Installation
Use this one-liner script in your terminal to install dependencies, and the program itself.
```
bash <(curl -sSL https://raw.githubusercontent.com/NotHavocc/pifmtx-neo/main/install.sh)
```
## Functions
This program supports a multitude of different transmitting options, like:
- SSTV (colored and grayscale)
- raw audio (.wav but others autoconvert)
- jammer (USE WITH CAUTION!!!!!!!!)

## Usage
It is reccomended to use the **pifmtx-neo** python script that you (probably) put in PATH when the setup asked to. The script can start the webserver with
```
pifmtx-neo start
```
and enable [autostart](https://github.com/NotHavocc/pifmtx-neo/edit/main/README.md#enabling-autostart) with
```
pifmtx-neo autostart
```
The default IP for the webserver is the local IP of the raspberry pi (the same one you use to, for example, ssh into it), or localhost (`127.0.0.1`) if you want to directly access from the pi itself. The port is `5000`
> [!NOTE]
> The Pi needs to be on the same WiFi connection as the device which you want to access the web dashboard on. (unless you port forward it, which is not reccomended.)

## Enabling autostart
This program has a built-in script that automatically creates a systemd service, thus enables auto startup when the pi starts. It is activated with the autostart command within the [Usage](https://github.com/NotHavocc/pifmtx-neo/edit/main/README.md#usage) tab of this readme.

## Issues
If you have any issues or reccomendations for this program, please leave an issue on this repository or contact me on my discord: nothavoc.


