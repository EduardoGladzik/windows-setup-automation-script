import subprocess
import os
import winreg

def is_installed(software_name):
    """
    Checks if a software is installed on the system
    by searching in the Windows registry.
    """
    # Common locations where uninstall information is stored
    subkeys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for subkey in subkeys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    software_key_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, software_key_name) as software_key:
                        try:
                            display_name = winreg.QueryValueEx(software_key, "DisplayName")[0]
                            if software_name.lower() in display_name.lower():
                                return True
                        except FileNotFoundError:
                            continue
        except FileNotFoundError:
            continue
    return False

def install_softwares():
    print("--- Starting software installation from local files ---")

    # Dictionary with software and their local paths
    software_list = {
        "7zip": {
            "local_path": r"instaladores\7z2501-x64.exe",
            "silent_parameter": "/S",
            "verification_name": "7-Zip"
        },
        "Google Chrome": {
            "local_path": r"instaladores\ChromeSetup.exe",
            "silent_parameter": "/S",
            "verification_name": "Google Chrome"
        },
        "Mozilla Firefox": {
            "local_path": r"instaladores\Firefox Installer.exe",
            "silent_parameter": "-ms",
            "verification_name": "Mozilla Firefox"
        },
        "Java": {
            "local_path": r"instaladores\jre-8u461-windows-x64.exe",
            "silent_parameter": "/qn",
            "verification_name": "Java"
        },
        "Adobe Reader": {
            "local_path": r"instaladores\Reader_br_install.exe",
            "silent_parameter": "/S",
            "verification_name": "Adobe Acrobat"
        }
    }
    
    for name, data in software_list.items():
        # Check if the software is already installed
        if is_installed(data["verification_name"]):
            print(f"\n{name} is already installed. Skipping installation.")
            continue
        
        # Check if the installation file exists in the local path
        if not os.path.exists(data["local_path"]):
            print(f"\nWarning: Installation file for {name} not found at '{data['local_path']}'. Skipping installation.")
            continue

        # Execute silent installation
        print(f"\nStarting installation of {name}...")
        try:
            command = [data["local_path"], data["silent_parameter"]]
            subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print(f"{name} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {name}: {e}")
        except FileNotFoundError:
            print(f"Error: Installation file for {name} not found.")