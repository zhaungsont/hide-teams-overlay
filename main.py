import subprocess

version = "0.1.0"


def main():
    print("Hide/Show Teams Overlay v" + version + " by Michael Chuang")
    all_process_names = get_all_process_names()
    teams_processes = filter_teams_processes(all_process_names)
    # print: Detected n Teams-related processes, and iterate through the list
    if len(teams_processes):
        print(f"Detected {len(teams_processes)} Teams-related processes:")
        for process in teams_processes:
            print(process)
        print("Toggling visibility of Teams windows...")
        toggle_teams_windows_visibility(teams_processes)
        print("Done! Feel free to close this window.")
    else:
        print("No Teams-related processes detected.")


def toggle_teams_windows_visibility(process_names):
    # Check visibility of the first process to determine action
    check_script = f"""
    tell application "System Events"
        set proc to first process whose name is "{process_names[0]}"
        return visible of proc
    end tell
    """
    check_output = subprocess.run(
        ["osascript", "-e", check_script], capture_output=True, text=True
    ).stdout.strip()

    # Determine whether to hide or show based on current state
    action = "false" if check_output == "true" else "true"

    if action == "true":
        print("Showing all Microsoft Teams windows")
    else:
        print("Hiding all Microsoft Teams windows")

    # Toggle visibility for all processes
    for process_name in process_names:
        toggle_script = f"""
        tell application "System Events"
            set processList to every process whose name is "{process_name}"
            repeat with proc in processList
                set visible of proc to {action}
            end repeat
        end tell
        """
        subprocess.run(["osascript", "-e", toggle_script])


def get_all_process_names():
    script = """
    tell application "System Events"
        set allProcesses to name of every process
        return allProcesses
    end tell
    """
    output = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return output.stdout.split(", ")


def filter_teams_processes(process_names):
    teams_processes = [name for name in process_names if "teams" in name.lower()]
    return teams_processes


def hide_process_windows(process_names):
    for process_name in process_names:
        script = f"""
        tell application "System Events"
            set processList to every process whose name is "{process_name}"
            repeat with proc in processList
                set visible of proc to false
            end repeat
        end tell
        """
        subprocess.run(["osascript", "-e", script])
        print("Hiding all Microsoft Teams windows")


def show_process_windows(process_names):
    for process_name in process_names:
        script = f"""
        tell application "System Events"
            set processList to every process whose name is "{process_name}"
            repeat with proc in processList
                set visible of proc to true
            end repeat
        end tell
        """
        subprocess.run(["osascript", "-e", script])
        print("Showing all Microsoft Teams windows")


if __name__ == "__main__":
    main()
