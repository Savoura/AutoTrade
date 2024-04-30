# PhBot AutoTrading Plugin

This plugin automates the process of trading. It records cursor positions for various interactions including opening the shop, selling items, confirming sales, and buying items. After completing the trading loop, it returns to the original town and repeats the process until reaching a specified trading threshold. It only works if the server doesn't have captcha and just disables auto buying using bots.

## Features

- **Cursor Position Recording**: Records cursor positions for specific interactions with NPC shops.
- **Automated Trading Loop**: Executes a trading loop by interacting with NPC shops based on recorded cursor positions.
- **Foreground Focus**: Brings the game window to the foreground to ensure accurate interactions.

## Getting Started

### Prerequisites

To use this script, you need to have the following:

- [pyautogui](https://pyautogui.readthedocs.io/en/latest/install.html) library
- [win32ctypes](https://pywin32-ctypes.readthedocs.io/en/latest/) library

These libraries can be installed via pip:

```bash
pip install pyautogui
pip install win32ctypes
```

Make sure you are using python 3.8 to be compatible with PhBot.

## Usage

1. Make sure you have 2 scripts for the 2 towns you want to trade between.
2. Add this line to the end of both scripts.
```
wait,2000
inject,<opcode>,<data>
wait,2000
switch_scripts
```
replace the `<opcode>` and `<data>` with the actual values of the current town NPC.

You can find the opcode & data using any Plugin such as PacketLogger

So the script would look something like this example :
```
walk,147,72,244
walk,149,84,243
wait,2000
inject,7046,F1,00,00,00,0C
wait,2000
switch_scripts
```
3. Add the directory of these scripts in the script input position.
4. Try talking with the Trading NPC to add the specific coords for the cursor.
5. Configure the script by setting the trading threshold and adjusting any other parameters as needed.
6. Press on `Start Script`:
7. Follow any prompts or instructions provided by the plugin.
8. Sit back and let the script automate the trading.
