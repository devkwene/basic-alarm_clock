import datetime
import time
import threading
import os

ALARM_FILE = "alarms.txt"

def load_alarms():
    if not os.path.exists(ALARM_FILE):
        return []

    alarms = []
    with open(ALARM_FILE, "r") as file:
        for line in file:
            time_part, message = line.strip().split(" | ")
            alarms.append({"time": time_part, "message": message})
    return alarms

def save_alarms(alarms):
    with open(ALARM_FILE, "w") as file:
        for alarm in alarms:
            file.write(f"{alarm['time']} | {alarm['message']}\n")

def alarm_thread(alarm_time, message):
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == alarm_time:
            print(f"\n⏰ ALARM! {message} ⏰\n")
            os.system("play -nq -t alsa synth 0.3 sine 880")  # Linux sound
            break
        time.sleep(20)  # check every 20 sec

def add_alarm():
    time_input = input("Enter alarm time (HH:MM): ").strip()
    message = input("Enter message for alarm: ").strip()

    alarms = load_alarms()
    alarms.append({"time": time_input, "message": message})
    save_alarms(alarms)

    print("\nAlarm added successfully!\n")

def show_alarms():
    alarms = load_alarms()
    if not alarms:
        print("\nNo alarms set.\n")
        return

    print("\nCurrent Alarms:")
    print("------------------------")
    for i, a in enumerate(alarms, 1):
        print(f"{i}. {a['time']} → {a['message']}")
    print()

def delete_alarm():
    alarms = load_alarms()
    show_alarms()

    if not alarms:
        return

    try:
        index = int(input("Enter alarm number to delete: "))
        if 1 <= index <= len(alarms):
            removed = alarms.pop(index - 1)
            save_alarms(alarms)
            print(f"\nDeleted alarm: {removed['time']} → {removed['message']}\n")
        else:
            print("\nInvalid number.\n")
    except ValueError:
        print("\nPlease enter a valid number.\n")

def start_alarm_checker():
    alarms = load_alarms()
    for alarm in alarms:
        t = threading.Thread(target=alarm_thread, args=(alarm["time"], alarm["message"]))
        t.daemon = True
        t.start()

def main():
    print("⏰ ADVANCED PYTHON ALARM CLOCK ⏰")

    start_alarm_checker()

    while True:
        print("\nMenu:")
        print("1. Add alarm")
        print("2. Show alarms")
        print("3. Delete alarm")
        print("4. Exit")

        choice = input("\nEnter choice (1–4): ").strip()

        if choice == "1":
            add_alarm()
        elif choice == "2":
            show_alarms()
        elif choice == "3":
            delete_alarm()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("\nInvalid choice. Try again.\n")

if __name__ == "__main__":
    main()
