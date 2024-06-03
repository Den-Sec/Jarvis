

# tools.py

import time
from googlesearch import search
from spotify_playback import play_item_by_name_and_artist
from task_management import add_task, list_tasks, check_reminders
from memory_management import add_memory, get_memory, list_memories

def parse_command(command):
    if not command.strip():
        print("Empty command received, ignoring.")
        return

    cmd_parts = command.split(" ")
    base_command = cmd_parts[0]

    if base_command == "print":
        print("Hello World!")
    elif base_command == "light1-on":
        print("Turning on the light")
    elif base_command == "light1-off":
        print("Turning off the light")
    elif base_command == "google":
        if len(cmd_parts) < 2:
            print("Google search command is incomplete.")
            return
        search_query = " ".join(cmd_parts[1:])
        print(f"Google search for: {search_query}")
        for j in search(search_query, num=5, stop=5):
            print(j)
    elif base_command == "spotify":
        if len(cmd_parts) < 2:
            print("Spotify command is incomplete.")
            return
        song_and_artist = " ".join(cmd_parts[1:]).split(" by ")
        if len(song_and_artist) == 2:
            song_name, artist_name = song_and_artist
        else:
            song_name = song_and_artist[0]
            artist_name = None
        print(f"Sending {song_name} by {artist_name} to Spotify")
        play_item_by_name_and_artist(song_name, artist_name)
    elif base_command == "add-task":
        if len(cmd_parts) < 2:
            print("Add-task command is incomplete.")
            return
        task_description = " ".join(cmd_parts[1:])
        add_task(task_description)
    elif base_command == "list-tasks":
        list_tasks()
    elif base_command == "remember":
        if len(cmd_parts) < 3:
            print("Remember command is incomplete.")
            return
        memory_key = cmd_parts[1]
        memory_info = " ".join(cmd_parts[2:])
        add_memory(memory_key, memory_info)
    elif base_command == "recall":
        if len(cmd_parts) < 2:
            print("Recall command is incomplete.")
            return
        memory_key = cmd_parts[1]
        memory_info = get_memory(memory_key)
        if memory_info:
            print(f"Memory: {memory_info['information']} (Added on: {memory_info['timestamp']})")
        else:
            print(f"No memory found for key: {memory_key}")
    elif base_command == "list-memories":
        list_memories()
    elif base_command in ["exit", "goodbye", "shutdown"]:
        print("Exiting program")
        exit()
    else:
        print("Invalid command")

if __name__ == "__main__":
    while True:
        command = input("Enter command: ")
        parse_command(command)
        check_reminders()
        time.sleep(60)
