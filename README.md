# BUZZ! Controller System - Setup Guide

This system lets you use smartphones as Buzz! quiz controllers for PCSX2 on Windows. It works by mapping button presses as keyboard presses for the emulator. The phones must be on the same network as the PC running the game and server.   

The code was fully generated using Claude AI (Sonnet 4.5) and has been tested and working.
  
  

<img src="https://github.com/user-attachments/assets/aa0317aa-c1f6-4ff0-b7d8-a193eb316ada" width="250">


## Files Included

1. `buzz_controller.html` - Web-based controller interface (open on phones)
2. `buzz_server.py` - Python server that runs on your PC
3. `requirements.txt` - Python dependencies
4. `SETUP.md` - This file
5. `Buzz 1-8 Mapping.ini` - Button mapping file for PCSX2

## Setup Instructions

### Part 1: Install Python (if needed)

1. Download Python from: https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation: Open Command Prompt and type `python --version`

### Part 2: Install Required Packages

1. Open Command Prompt **as Administrator** (right-click → "Run as administrator")
2. Navigate to the folder containing these files:
   ```
   cd C:\path\to\buzz_controller_folder
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Part 3: Configure PCSX2

**PCSX2 Must be Version 2.6 or higher !!**  
_(Older versions have bugs with buzz controllers and those bugs are also present when using USBqemu-wheel for even older versions)_

1. Copy Buzz 1-8 Mapping.ini to inputprofiles-folder. For standard installations, this is located in Documents\PCSX2\inputprofiles. In portable mode, it resides in the inis folder within the installation directory. 
2. Open PCSX2
3. In the top menu, go to **Settings → Controllers**
4. In the bottom section, choose Buzz 1-8 Mapping from the drop down menu
5. You should see buzz controllers in the left menu in USB Ports

### Part 4: Start the Server

1. Open Command Prompt **as Administrator**
2. Navigate to the folder:
   ```
   cd C:\path\to\buzz_controller_folder
   ```
3. Run the server:
   ```
   python buzz_server.py
   ```
4. You should see:
   ```
   ============================================================
   BUZZ! Controller Server
   ============================================================
   Server starting on ws://localhost:8765
   Waiting for connections...
   ============================================================
   ```

**Important:** Keep this Command Prompt window open while playing!

### Part 5: Open Controllers on Phones

#### Option A: Using Python's Built-in Web Server (Easiest)

1. Open a **second** Command Prompt window
2. Navigate to the folder containing `buzz_controller.html`:
   ```
   cd C:\path\to\buzz_controller_folder
   ```
3. Start a simple web server:
   ```
   python -m http.server 8080
   ```
4. Find your PC's IP address:
   - Open Command Prompt
   - Type: `ipconfig`
   - Look for "IPv4 Address" (usually starts with 192.168.x.x)
5. On each phone:
   - Open a web browser
   - Go to: `http://YOUR_PC_IP:8080/buzz_controller.html`
   - Example: `http://192.168.1.100:8080/buzz_controller.html`
6. On each phone, tap the **gear icon** (⚙️) in the top right
7. Select the controller number (1-8)
8. Tap "Done"

**Tip:** Use an online qr code generator or url shortener to make it easier for players to connect to the server.

#### Option B: Direct File Access (Alternative)

1. Transfer `buzz_controller.html` to each phone
2. Open it in a browser
3. **Before playing**, you need to modify the file:
   - Open the HTML file in a text editor
   - Find the line: `const SERVER_URL = 'ws://localhost:8765';`
   - Change `localhost` to your PC's IP address
   - Example: `const SERVER_URL = 'ws://192.168.1.100:8765';`
   - Save and reload on phones

### Part 6: Start Playing!

1. Make sure the server is running on your PC
2. Make sure all phones show "Connected" (in green)
3. Each player should have selected their controller number (P1-P8)
4. Start your Buzz! game in PCSX2
5. Test the buttons - they should work!


## Troubleshooting

### Phones won't connect / "Disconnected" status

**Check 1: Firewall**
- Windows Firewall might be blocking connections
- When you first run the server, Windows may ask to allow access - click "Allow"
- If you didn't see this, manually allow Python through firewall:
  1. Open "Windows Security" → "Firewall & network protection"
  2. Click "Allow an app through firewall"
  3. Find Python and check both "Private" and "Public"

**Check 2: Network**
- Make sure your PC and phones are on the **same WiFi network**
- Some guest WiFi networks block device communication

**Check 3: IP Address**
- Double-check your PC's IP address with `ipconfig`
- Make sure you're using the correct IP in the browser

### Buttons don't work in PCSX2

1. Make sure PCSX2 window is in focus (click on it)
2. Check that you configured the controller bindings in PCSX2 settings
3. Test that the keys work - when you press a button on the phone, the server should print messages
4. Make sure the server is running **as Administrator**

### Blue button is pressing by itself or other similar input errors in-game  
- These bugs have been resolved in the PCSX2 release, check if you are on an older version.

### "ModuleNotFoundError" when running server

- You need to install the dependencies:
  ```
  pip install -r requirements.txt
  ```
- Make sure you're running Command Prompt as Administrator

### Server crashes or keys get stuck

- Restart the server (close Command Prompt and run `python buzz_server.py` again)
- This releases any stuck keys


## Advanced: Running on Network

By default, the server listens on all network interfaces (0.0.0.0), so any device on your local network can connect.

**Security Note:** This is only accessible on your local network. Don't expose port 8765 to the internet.

## Having Issues?

The server prints helpful debug messages when buttons are pressed:
```
[14:23:45] P1 - BUZZER: PRESS (key: q)
[14:23:45] P1 - BUZZER: RELEASE (key: q)
```

This helps you see if:
1. The phone is connecting properly
2. Button presses are being received
3. The correct keys are being sent

If you see these messages but PCSX2 doesn't respond, the issue is with PCSX2's controller configuration.

## Customizing Key Mappings

If you want to use different keys:

1. Open `buzz_server.py` in a text editor
2. Find the `KEY_MAPPINGS` section at the top
3. Change the keys to whatever you want
4. Save the file
5. Restart the server
6. Update your PCSX2 controller bindings to match

### Key Mappings

These are the default bindings for the app.  
These have been modified for scandinavian keyboard and there might be some issues for other locales.

**Note:** You can modify these key mappings in `buzz_server.py` if you prefer different keys. Directions in another section below.

**Player 1:**
- Buzzer: Q
- Blue: W
- Orange: E
- Green: R
- Yellow: T

**Player 2:**
- Buzzer: A
- Blue: S
- Orange: D
- Green: F
- Yellow: G

**Player 3:**
- Buzzer: Z
- Blue: X
- Orange: C
- Green: V
- Yellow: B

**Player 4:**
- Buzzer: Y
- Blue: U
- Orange: I
- Green: O
- Yellow: P

**Player 5:**
- Buzzer: H
- Blue: J
- Orange: K
- Green: L
- Yellow: ;

**Player 6:**
- Buzzer: N
- Blue: M
- Orange: §
- Green: +
- Yellow: <

**Player 7:**
- Buzzer: 1
- Blue: 2
- Orange: 3
- Green: 4
- Yellow: 5

**Player 8:**
- Buzzer: 6
- Blue: 7
- Orange: 8
- Green: 9
- Yellow: 0


## Enjoy!

Have fun playing Buzz! with up to 8 players using your smartphones as controllers!
