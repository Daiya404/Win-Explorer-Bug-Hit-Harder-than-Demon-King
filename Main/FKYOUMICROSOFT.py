import sys
import ctypes
import ctypes.wintypes
import time
from pathlib import Path
from datetime import datetime
from threading import Thread

# === A Useless Goddess's Blessings on This Wonderful Code! ===
# Kazuma: "I came to a parallel world, and now I'm stuck debugging Python scripts.
# At least it's better than being eaten by giant toads."

# --- Party Member Constants ---
# Aqua: "Hey! I'm a goddess! My stats should be maxed out! Why am I just a modifier?"
# Kazuma: "Because you're only useful in very specific, annoying situations."
MOD_KAZUMA_STEAL = 0x0002  # More commonly known as MOD_CONTROL. Kazuma's steady hand for... acquiring things.
MOD_DARKNESS_TAUNT = 0x0004  # MOD_SHIFT. She's shifting the enemy's focus... by being a total masochist.

# --- Spell & Hotkey Definitions ---
# Megumin: "My ultimate spell requires a specific incantation!"
WM_EXPLOSION = 0x0312  # This is our magic spell's identifier, WM_HOTKEY.
VK_F12_CAST_EXPLOSION = 0x7B # The F12 key, the trigger for our daily EXPLOSION!

# A unique ID for our party's ultimate skill.
ADVENTURER_GUILD_QUEST_ID = 1

# --- The Adventurer's Guild Scribe (Logging) ---
# Luna: "Please log your party's activities responsibly. And try not to destroy the town... again."
def chronicle_quest(message):
    """Logs our party's heroic (or pathetic) deeds."""
    log_scroll = Path.home() / 'AdventurerGuild.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(log_scroll, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        # Kazuma: "Probably some Dullahan's curse. Or maybe the disk is full. Whatever."
        pass

# --- Megumin's Daily Explosion Cooldown ---
# Megumin needs time to recover her mana after one cast. It's a one-shot deal.
last_explosion_time = 0
mana_recovery_time = 4.0  # Increased cooldown for a more powerful... effect.

def cast_explosion_magic():
    """
    The moment we've all been waiting for. The pinnacle of Crimson Demon magic!
    """
    global last_explosion_time
    current_time = time.time()
    
    if current_time - last_explosion_time < mana_recovery_time:
        chronicle_quest("Megumin is out of mana! She's collapsed and can't cast Explosion again so soon!")
        return
        
    last_explosion_time = current_time
    chronicle_quest("DARKNESS BLACKER THAN BLACK AND DARKER THAN DARK...")
    chronicle_quest("I BESEECH THEE, COMBINE WITH MY DEEP CRIMSON.")
    chronicle_quest("THE TIME OF AWAKENING COMETH.")
    chronicle_quest("JUSTICE, FALLEN UPON THE INFALLIBLE BOUNDARY,")
    chronicle_quest("APPEAR NOW AS AN INTANGIBLE DISTORTION!")
    chronicle_quest("I DESIRE FOR MY ULTIMATE, UNPARALLELED, AND UNRIVALED POWER...")
    chronicle_quest("A POWER AS DESTRUCTIVE AS TO CRUMBLE ALL OF CREATION...")
    chronicle_quest("A POWER THAT WILL PIERCE THE VERY HEAVENS!")
    chronicle_quest("FROM THE ABYSS, I CALL TO THEE...")
    chronicle_quest("IN THE NAME OF THE GREATEST ARCH-WIZARD OF THE CRIMSON DEMONS...")
    chronicle_quest("LET THE APOCALYPSE BE UNLEASHED UPON THIS REALM...")
    chronicle_quest("THIS IS THE ULTIMATE DESTRUCTIVE POWER!")
    chronicle_quest("EXPLOSION!")
    
    # Run the actual command in a separate thread, like Kazuma carrying Megumin home.
    Thread(target=summon_emergency_quest_terminal, daemon=True).start()

def summon_emergency_quest_terminal():
    """
    Kazuma: "Great, she blew something up. Now I have to deal with the aftermath.
    This better be a high-reward quest."
    """
    try:
        # This command string is like a quest objective given by the guild.
        quest_details = '/k "echo A wild CMD terminal appears! & echo It was super effective! & timeout /t 2 /nobreak >nul & exit"'
        # We need admin rights because, let's face it, our party is a walking disaster.
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", quest_details, None, 1)
    except Exception as e:
        # Aqua is probably crying somewhere about this.
        chronicle_quest(f"✗ Aqua's Useless Goddess Powers failed! Exception: {e}")

def main_quest():
    """
    The main storyline of our dysfunctional party.
    """
    chronicle_quest("=" * 70)
    chronicle_quest("KonoSuba: God's Blessing on This Wonderful Hotkey!")
    chronicle_quest("Quest: Register the 'EXPLOSION' Hotkey (Ctrl+Shift+F12).")
    chronicle_quest("Reward: A slightly more convenient way to open CMD.")
    chronicle_quest("=" * 70)

    # Kazuma: "Try not to screw this up, Aqua."
    # We unregister the hotkey on exit to avoid angering the gods (or Windows).
    try:
        chronicle_quest("Talking to the Adventurer's Guild to register our party's ultimate skill...")
        
        # This is where we combine our party's... unique talents.
        if not ctypes.windll.user32.RegisterHotKey(None, ADVENTURER_GUILD_QUEST_ID, MOD_KAZUMA_STEAL | MOD_DARKNESS_TAUNT, VK_F12_CAST_EXPLOSION):
            error_message = "✗ Failed to register hotkey! Some other party (or program) probably took the quest already."
            chronicle_quest(error_message)
            # Aqua starts wailing.
            ctypes.windll.user32.MessageBoxW(0, "Waaah! Someone stole our hotkey!\nIt's probably the Demon King's fault!", "Useless Goddess Error", 0x10)
            return 1 # Quest Failed.
            
        chronicle_quest("✓ Quest Accepted! Our 'EXPLOSION' hotkey is ready. Waiting for a worthy target (or, you know, just a key press).")
        
        # The eternal loop of waiting for a quest, like sitting in the guild hall.
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_EXPLOSION:
                if msg.wParam == ADVENTURER_GUILD_QUEST_ID:
                    cast_explosion_magic()

    except Exception as e:
        # Kazuma: "Great. Just great. Another disaster. I'm surrounded by idiots."
        chronicle_quest(f"CRITICAL ERROR! The whole party wiped! {e}")
        return 1
        
    finally:
        # Cleaning up is important, or we'll get a massive bill from the town.
        chronicle_quest("The quest is over. Returning to the guild and unregistering the skill.")
        ctypes.windll.user32.UnregisterHotKey(None, ADVENTURER_GUILD_QUEST_ID)
        chronicle_quest("✓ Cleanup complete. Now, let's go get a drink.")
            
    return 0 # Quest Complete!

if __name__ == '__main__':
    # Kazuma: "Hai, Kazuma desu."
    sys.exit(main_quest())