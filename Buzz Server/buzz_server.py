import asyncio
import websockets
import json
import keyboard
from datetime import datetime

# Key mapping for each controller (1-8) and button
# Modify these key mappings to match your PCSX2 configuration
KEY_MAPPINGS = {
    1: {
        'buzzer': 'q',
        'blue': 'w',
        'orange': 'e',
        'green': 'r',
        'yellow': 't'
    },
    2: {
        'buzzer': 'a',
        'blue': 's',
        'orange': 'd',
        'green': 'f',
        'yellow': 'g'
    },
    3: {
        'buzzer': 'z',
        'blue': 'x',
        'orange': 'c',
        'green': 'v',
        'yellow': 'b'
    },
    4: {
        'buzzer': 'y',
        'blue': 'u',
        'orange': 'i',
        'green': 'o',
        'yellow': 'p'
    },
    5: {
        'buzzer': 'h',
        'blue': 'j',
        'orange': 'k',
        'green': 'l',
        'yellow': "'"
    },
    6: {
        'buzzer': 'n',
        'blue': 'm',
        'orange': '§',
        'green': '+',
        'yellow': '<'
    },
    7: {
        'buzzer': '1',
        'blue': '2',
        'orange': '3',
        'green': '4',
        'yellow': '5'
    },
    8: {
        'buzzer': '6',
        'blue': '7',
        'orange': '8',
        'green': '9',
        'yellow': '0'
    }
}

connected_clients = set()
pressed_keys = {}  # Track which keys are currently pressed

async def handle_client(websocket, path):
    """Handle incoming WebSocket connections"""
    connected_clients.add(websocket)
    client_addr = websocket.remote_address
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Client connected: {client_addr}")
    
    try:
        async for message in websocket:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] RAW MESSAGE RECEIVED: {message}")  # DEBUG
            try:
                data = json.loads(message)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] PARSED DATA: {data}")  # DEBUG
                controller = data.get('controller')
                button = data.get('button')
                pressed = data.get('pressed')
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Controller={controller}, Button={button}, Pressed={pressed}")  # DEBUG
                
                if controller in KEY_MAPPINGS and button in KEY_MAPPINGS[controller]:
                    key = KEY_MAPPINGS[controller][button]
                    key_id = f"{controller}_{button}"
                    
                    if pressed and key_id not in pressed_keys:
                        # Press the key
                        keyboard.press(key)
                        pressed_keys[key_id] = key
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] P{controller} - {button.upper()}: PRESS (key: {key})")
                    
                    elif not pressed and key_id in pressed_keys:
                        # Release the key
                        keyboard.release(key)
                        del pressed_keys[key_id]
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] P{controller} - {button.upper()}: RELEASE (key: {key})")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: Invalid controller ({controller}) or button ({button})")  # DEBUG
                
            except json.JSONDecodeError as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Invalid JSON received: {e}")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Message was: {message}")
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error processing message: {e}")
                import traceback
                traceback.print_exc()
    
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Client disconnected: {client_addr}")
        
        # Release any keys that were pressed by this client
        # (In a production app, you'd want to track which client pressed which keys)
        for key in list(pressed_keys.values()):
            try:
                keyboard.release(key)
            except:
                pass
        pressed_keys.clear()

async def main():
    print("=" * 60)
    print("BUZZ! Controller Server")
    print("=" * 60)
    print("\nKey Mappings (configure these in PCSX2):")
    print("-" * 60)
    
    for controller_num in range(1, 9):
        print(f"\nPlayer {controller_num}:")
        for button, key in KEY_MAPPINGS[controller_num].items():
            print(f"  {button.upper():8} -> {key.upper()}")
    
    print("\n" + "=" * 60)
    print("Server starting on ws://localhost:8765")
    print("Waiting for connections...")
    print("=" * 60 + "\n")
    
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        # Release all pressed keys on exit
        for key in pressed_keys.values():
            try:
                keyboard.release(key)
            except:
                pass
