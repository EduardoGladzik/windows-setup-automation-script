import subprocess
import winreg

class Softwares():
    
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

    def install_softwares(name, data):
        """
        Install a list of softwares silently from local installation files.
        """
        try:
            command = [data["local_path"], data["silent_parameter"]]
            subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print(f"{name} instalado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao instalar {name}: {e}")