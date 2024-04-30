from phBot import *
import QtBind
import pyautogui
from threading import Timer
import ctypes

pVersion = 'v0.1.1'
pName = 'AutoTrade'
pUrl = 'https://raw.githubusercontent.com/Savoura/AutoTrade/main/AutoTrade.py'

# Global Variables
inGame = None
count = 0
defaultTradeLimit = '10'
script_running = False
current_script = True
first_script = None
second_script = None
stop_packet = False
ongoing_processes = []

# GUI
gui = QtBind.init(__name__, pName)
firstTextScriptPath = QtBind.createLineEdit(gui, '', 15, 30, 500, 20)
secondTextScriptPath = QtBind.createLineEdit(gui, '', 15, 60, 500, 20)

btnStart = QtBind.createButton(gui, 'start_clicked', '  Start Script  ', 20, 90)
btnStop = QtBind.createButton(gui, 'stop_clicked', '  Stop Script  ', 150, 90)

totalLabel = QtBind.createLabel(gui, 'Total trades done :  ', 15, 230)
currentCntLabel = QtBind.createLabel(gui, str(count), 130, 230)

tradeLimitLabel = QtBind.createLabel(gui, 'Trade Limit : ', 15, 250)
tradeLimitLine = QtBind.createLineEdit(gui, defaultTradeLimit, 100, 250, 30, 20)

warningLabel = QtBind.createLabel(gui, 'Only stop Script when it is walking never stop it when it is clicking to not crash!!', 15, 280)
hintLabel = QtBind.createLabel(gui, 'To record coordinates, click on the button and wait 5 seconds while placing the cursor on the desired location.', 15, 300)

# Positions GUI
sellRecordBtn = QtBind.createButton(gui, 'record_sell_coords', ' Record Sell ', 40, 160)
sellXLabel = QtBind.createLabel(gui, 'Sell all X:', 15, 130)
sellXText = QtBind.createLineEdit(gui, '', 65, 130, 30, 20)
sellYLabel = QtBind.createLabel(gui, 'Sell all Y:', 15, 190)
sellYText = QtBind.createLineEdit(gui, '', 65, 190, 30, 20)

confirmRecordBtn = QtBind.createButton(gui, 'record_confirm_coords', ' Record Confirm ', 130, 160)
confirmXLabel = QtBind.createLabel(gui, 'Confirm X:', 105, 130)
confirmXText = QtBind.createLineEdit(gui, '', 170, 130, 30, 20)
confirmYLabel = QtBind.createLabel(gui, 'Confirm Y:', 105, 190)
confirmYText = QtBind.createLineEdit(gui, '', 170, 190, 30, 20)

buyXRecordBtn = QtBind.createButton(gui, 'record_buy_coords', ' Record Buy ', 240, 160)
buyXLabel = QtBind.createLabel(gui, 'Buy loot X:', 215, 130)
buyXText = QtBind.createLineEdit(gui, '', 270, 130, 30, 20)
buyYLabel = QtBind.createLabel(gui, 'Buy loot Y:', 215, 190)
buyYText = QtBind.createLineEdit(gui, '', 270, 190, 30, 20)

shopStartRecordBtn = QtBind.createButton(gui, 'shop_start_record_coords', ' Record Shop1 ', 330, 160)
shopStartXLabel = QtBind.createLabel(gui, 'Shop1 X:', 305, 130)
shopStartXText = QtBind.createLineEdit(gui, '', 360, 130, 30, 20)
shopStartYLabel = QtBind.createLabel(gui, 'Shop1 Y:', 305, 190)
shopStartYText = QtBind.createLineEdit(gui, '', 360, 190, 30, 20)

shopEndRecordBtn = QtBind.createButton(gui, 'shop_end_record_coords', ' Record Shop2 ', 430, 160)
shopEndXLabel = QtBind.createLabel(gui, 'Shop2 X:', 405, 130)
shopEndXText = QtBind.createLineEdit(gui, '', 460, 130, 30, 20)
shopEndYLabel = QtBind.createLabel(gui, 'Shop2 Y:', 405, 190)
shopEndYText = QtBind.createLineEdit(gui, '', 460, 190, 30, 20)

# Function to record coordinates and update text boxes
def shop_start_record_coords():
    Timer(5.0, get_coords, [shopStartXText, shopStartYText]).start()

def shop_end_record_coords():
    Timer(5.0, get_coords, [shopEndXText, shopEndYText]).start()
    
def record_sell_coords():
    Timer(5.0, get_coords, [sellXText, sellYText]).start()

def record_confirm_coords():
    Timer(5.0, get_coords, [confirmXText, confirmYText]).start()

def record_buy_coords():
    Timer(5.0, get_coords, [buyXText, buyYText]).start()
    
def get_coords(shopXText, shopYText):
    x, y = pyautogui.position()
    QtBind.setText(gui, shopXText, str(x))
    QtBind.setText(gui, shopYText, str(y))

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

def open_shop(stop, currScript):
    if currScript:  # If currScript is True, use shopEnd coordinates
        shopX = int(QtBind.text(gui, shopEndXText))
        shopY = int(QtBind.text(gui, shopEndYText))
    else:  # Otherwise, use shopStart coordinates
        shopX = int(QtBind.text(gui, shopStartXText))
        shopY = int(QtBind.text(gui, shopStartYText))

    pyautogui.click(shopX, shopY)
        
    Timer(2.0, lambda: sell_loot(stop)).start()

def sell_loot(stop):
    sellX = int(QtBind.text(gui, sellXText))
    sellY = int(QtBind.text(gui, sellYText))
    confirmX = int(QtBind.text(gui, confirmXText))
    confirmY = int(QtBind.text(gui, confirmYText))
    
    pyautogui.click(x=sellX, y=sellY)
    Timer(3.0, lambda:pyautogui.click(x=confirmX, y=confirmY)).start()
    Timer(10.0, lambda:buy_loot(stop)).start()

def buy_loot(stop):
    if stop:
        return 0
    
    buyX = int(QtBind.text(gui, buyXText))
    buyY = int(QtBind.text(gui, buyYText))

    pyautogui.keyDown('ctrl')
    pyautogui.click(x=buyX, y=buyY)
    pyautogui.keyUp('ctrl')

    Timer(5.0, exit_shop).start()

def exit_shop():
    opcode, data = "0x704B", "00 00 00 00 0C"
    opcode_int = int(opcode, 16)
    
    data_bytes = bytearray(int(byte, 16) for byte in data.split())
    inject_joymax(opcode_int, data_bytes, False)

def bring_SRO_to_foreground():
    if inGame or isJoined():
        hwnd = ctypes.windll.user32.FindWindowW(None, f"[{inGame['server']}] {inGame['name']}")
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 5)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        return True
    else:
        log("Plugin works only when the client is visible.")
        return False

def stop_clicked():
    global script_running
    if script_running:
        script_running = False
        stop_script()
        log("Script stopped.")  
    else:
        log("Script not running.")

    
def start_clicked():
    global first_script, second_script, script_running, count, defaultTradeLimit
   
    defaultTradeLimit = int(QtBind.text(gui, tradeLimitLine))
    
    count = 0
    update_count_label()
    
    first_script_path = QtBind.text(gui, firstTextScriptPath)
    second_script_path = QtBind.text(gui, secondTextScriptPath)
    
    first_script = read_script_from_file(first_script_path)
    second_script = read_script_from_file(second_script_path)
    
    if script_running:
        log("Script already running.")
        return
    
    if first_script and second_script:
        start_script(first_script)
        log("Script started.")
        script_running = True


def Inject_SelectEntity(EntityID):
	inject_joymax(0x7045,struct.pack('<I',EntityID),False)

def Inject_ExitNpc(EntityID):
	inject_joymax(0x704B,struct.pack('<I',EntityID),False)

def FindNpcByExpression(_lambda):
	npcs = get_npcs()
	if npcs:
		for uid, npc in npcs.items():
			# Search by lambda
			if _lambda(npc['name'],npc['servername']):
				# Save unique id
				npc['entity_id'] = uid
				return npc
	return None

def NPC_talk(npc):
    entityID = npc['entity_id']
    Inject_SelectEntity(entityID)

def talk_with_npc():
    npcInfo = FindNpcByExpression(lambda n,s: '_SPECIAL' in s)
    if npcInfo:
        NPC_talk(npcInfo)
        log("talking with NPC")
    else:
        log("Plugin: Specialty Trader NPC is not near!")

def switch_scripts(args):
    global current_script, first_script, second_script, count, defaultTradeLimit, ongoing_processes
   
    count += 1
    update_count_label()    

    if count == defaultTradeLimit:
        if bring_SRO_to_foreground():
            talk_with_npc()
            Timer(1.0, open_shop, [True, current_script]).start()
        return 0
    
    if bring_SRO_to_foreground():
        talk_with_npc()
        Timer(1.0, open_shop, [False, current_script]).start()
        
    else:
        log("SRO not found. Stopping script.")
        return 0

    if current_script:
        current_script = False       
        Timer(20.0, lambda: start_script(second_script)).start()
        return 0
    else:
        current_script = True
        Timer(20.0, lambda: start_script(first_script)).start()
        return 0

# Plugin Loaded
log('Plugin: '+pName+' '+pVersion+' successfully loaded.')
