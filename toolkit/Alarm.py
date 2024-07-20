import time
import pygame
from threading import Thread
from datetime import datetime, timedelta
import re


alarm_active = False

def set_set_alarm(alarm_time, sound_file):
    global alarm_active
    while alarm_active:
        current_time = datetime.now()
        if current_time >= alarm_time:
            print("Good day, sir. It appears it is time for your scheduled alert as the alarm has been activated.")
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if not alarm_active:
                    pygame.mixer.music.stop()
                    return
                pygame.time.Clock().tick(10)
            break
        time.sleep(1)  # Check the time every second

def set_alarm(alarm_time, sound_file="audio/Sky High.mp3"):
    global alarm_active
    alarm_active = True
    print("ALARM SET FOR", alarm_time)
    Thread(target=set_set_alarm, args=(alarm_time, sound_file)).start()

def stop_alarm():
    global alarm_active
    alarm_active = False
    pygame.mixer.music.stop()
    print("ALARM STOPPED")

def parse_alarm_time(command):
    now = datetime.now()

    # Check for relative times
    match = re.search(r'(\d+)\s*(hours?|minutes?|seconds?|hrs?|mins?|secs?)\s*(later|from now|after)', command, re.IGNORECASE)
    if match:
        amount = int(match.group(1))
        unit = match.group(2).lower()
        
        if 'hour' in unit or 'hr' in unit:
            alarm_time = now + timedelta(hours=amount)
        elif 'minute' in unit or 'min' in unit:
            alarm_time = now + timedelta(minutes=amount)
        elif 'second' in unit or 'sec' in unit:
            alarm_time = now + timedelta(seconds=amount)
        
        return alarm_time

    # Check for absolute times with optional AM/PM
    match = re.search(r'(\d+):?(\d+)?\s*(am|pm)?', command, re.IGNORECASE)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        period = match.group(3)

        if period:
            if period.lower() == 'pm' and hour != 12:
                hour += 12
            elif period.lower() == 'am' and hour == 12:
                hour = 0

        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if "tomorrow" in command.lower():
            alarm_time += timedelta(days=1)
        elif alarm_time < now:
            alarm_time += timedelta(days=1)
        
        return alarm_time

    raise ValueError("Could not parse alarm time from command")

if __name__ == "__main__":
    try:
        command = input("Set an alarm: ")
        alarm_time = parse_alarm_time(command)
        set_alarm(alarm_time)
    except Exception as e:
        print(f"Error: {e}")
