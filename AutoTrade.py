from phBot import *
import QtBind
import pyautogui
from threading import Timer
import ctypes

pVersion = 'v0.1.0'
pName = 'AutoTrade'
pUrl = ''

inGame = None
count = 0
defaultTradeLimit = '10'
script_running = False
current_script = True
first_script = None
second_script = None
default_openX = '200'
default_openY = '520'
default_sellX = '1063'
default_sellY = '691'
default_confirmX = '916'
default_confirmY = '591'
default_buyX = '117'
default_buyY = '440'
default_exitX = '318'
default_exitY = '374'

# Needed for phbot GUI
gui = QtBind.init(__name__,pName)
firstTextScriptPath = QtBind.createLineEdit(gui, '', 15, 30, 500, 20)
secondTextScriptPath = QtBind.createLineEdit(gui, '', 15, 60, 500, 20)
btnStart = QtBind.createButton(gui, 'start_clicked', '  Start Script  ', 20, 90)
btnStop = QtBind.createButton(gui, 'stop_clicked', '  Stop Script  ', 150, 90)
totalLabel = QtBind.createLabel(gui, 'Total trades done :  ', 15, 200)
currentCntLabel = QtBind.createLabel(gui, str(count), 130, 200)
tradeLimitLabel = QtBind.createLabel(gui, 'Trade Limit : ', 15, 250)
tradeLimitLine = QtBind.createLineEdit(gui, defaultTradeLimit, 100, 250, 30, 20)

openXLabel = QtBind.createLabel(gui, 'Open shop X:', 15, 130)
openXText = QtBind.createLineEdit(gui, default_openX, 100, 130, 30, 20)  # Default value for openX
openYLabel = QtBind.createLabel(gui, 'Open shop Y:', 15, 170)
openYText = QtBind.createLineEdit(gui, default_openY, 100, 170, 30, 20)  # Default value for openY
sellXLabel = QtBind.createLabel(gui, 'Sell all X:', 145, 130)
sellXText = QtBind.createLineEdit(gui, default_sellX, 210, 130, 30, 20)  # Default value for sellX
sellYLabel = QtBind.createLabel(gui, 'Sell all Y:', 145, 170)
sellYText = QtBind.createLineEdit(gui, default_sellY, 210, 170, 30, 20)  # Default value for sellY
confirmXLabel = QtBind.createLabel(gui, 'Confirm X:', 275, 130)
confirmXText = QtBind.createLineEdit(gui, default_confirmX, 340, 130, 30, 20)  # Default value for confirmX
confirmYLabel = QtBind.createLabel(gui, 'Confirm Y:', 275, 170)
confirmYText = QtBind.createLineEdit(gui, default_confirmY, 340, 170, 30, 20)  # Default value for confirmY
buyXLabel = QtBind.createLabel(gui, 'Buy loot X:', 410, 130)
buyXText = QtBind.createLineEdit(gui, default_buyX, 475, 130, 30, 20)  # Default value for buyX
buyYLabel = QtBind.createLabel(gui, 'Buy loot Y:', 410, 170)
buyYText = QtBind.createLineEdit(gui, default_buyY, 475, 170, 30, 20)  # Default value for buyY
exitXLabel = QtBind.createLabel(gui, 'Exit X:', 545, 130)
exitXText = QtBind.createLineEdit(gui, default_exitX, 605, 130, 30, 20)  # Default value for exitX
exitYLabel = QtBind.createLabel(gui, 'Exit Y:', 545, 170)
exitYText = QtBind.createLineEdit(gui, default_exitY, 605, 170, 30, 20)  # Default value for exitY

# Create GUI elements


def update_count_label():
    global count
    QtBind.setText(gui, currentCntLabel, str(count))

def isJoined():
    global inGame
    inGame = get_character_data()
    if not (inGame and "name" in inGame and inGame["name"]):
        inGame = None
    return inGame

def read_script_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def sell_loot():
    # Read openX, openY, sellX, sellY, confirmX, and confirmY from GUI text fields
    openX = int(QtBind.text(gui, openXText))
    openY = int(QtBind.text(gui, openYText))
    sellX = int(QtBind.text(gui, sellXText))
    sellY = int(QtBind.text(gui, sellYText))
    confirmX = int(QtBind.text(gui, confirmXText))
    confirmY = int(QtBind.text(gui, confirmYText))
    
    Timer(2.0, lambda: pyautogui.click(x=openX, y=openY)).start()
    pyautogui.click(x=sellX, y=sellY)
    pyautogui.click(x=confirmX, y=confirmY)
    Timer(7.0, buy_loot).start()

def buy_loot():
    # Read buyX and exitX from GUI text fields
    buyX = int(QtBind.text(gui, buyXText))
    buyY = int(QtBind.text(gui, buyYText))
    exitX = int(QtBind.text(gui, exitXText))
    exitY = int(QtBind.text(gui, exitYText))

    pyautogui.keyDown('ctrl')
    pyautogui.click(x=buyX, y=buyY)
    pyautogui.keyUp('ctrl')

    Timer(5.0, lambda: pyautogui.click(x=exitX, y=exitY)).start()

def bring_SRO_to_foreground():
    if inGame or isJoined():
        hwnd = ctypes.windll.user32.FindWindowW(None, f"[{inGame['server']}] {inGame['name']}")
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 5)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    else:
        log("Plugin works only when the client is visible.")

def stop_clicked():
    global script_running
    stop_script()
    script_running = False
   
def start_clicked():
    global first_script, second_script, script_running, count, defaultTradeLimit
    
	 
    defaultTradeLimit = int(QtBind.text(gui, tradeLimitLine))
    
    count = 0
    first_script_path = QtBind.text(gui, firstTextScriptPath)
    second_script_path = QtBind.text(gui, secondTextScriptPath)
    first_script = read_script_from_file(first_script_path)
    second_script = read_script_from_file(second_script_path)
    
    if script_running:
        log("Script already running.")
        return
    
    if first_script and second_script:
        start_script(first_script)
        script_running = True
        
def switch_scripts(args):
    global current_script, first_script, second_script, count, defaultTradeLimit
    
    if count == defaultTradeLimit:
        return 0
    
    count += 1
    update_count_label()
    
    if current_script:
        bring_SRO_to_foreground()
        current_script = False
        sell_loot()
        Timer(5.0, lambda: start_script(second_script)).start()
        return 0
    else:
        bring_SRO_to_foreground()
        current_script = True
        sell_loot()
        Timer(5.0, lambda: start_script(first_script)).start()
        return 0
        

log('Plugin: '+pName+' '+pVersion+' successfully loaded.')
