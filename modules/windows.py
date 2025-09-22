import subprocess

class WindowsConfiguration():

    def disable_uac():
        """
        Disables User Account Control (UAC).
        """
        print("Disabling User Account Control (UAC)...")
        try:
            uac_command = 'Set-ItemProperty -Path "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "EnableLUA" -Value 0 -Force'
            subprocess.run(["powershell", "-Command", uac_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("UAC disabled successfully. The change will be applied on the next restart.")
        except subprocess.CalledProcessError as e:
            print(f"Error disabling UAC: {e}")

    def enable_rdp():
        """
        Enables Remote Desktop Connection.
        """
        print("\nEnabling Remote Desktop Connection...")
        try:
            rdp_command = 'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" -Name "fDenyTSConnections" -Value 0 -Force'
            subprocess.run(["powershell", "-Command", rdp_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Remote Desktop Connection enabled successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error enabling RDP: {e}")
            
    def adjust_performance_settings():
        print("\n--- Configurando o desempenho do Windows ---")
        try:
            # 1. Ajustar para melhor desempenho (muda para 'Melhor Desempenho')
            print("Ajustando para o modo 'Melhor Desempenho'...")
            performance_command = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v "VisualFXSetting" /t REG_DWORD /d 2 /f'
            subprocess.run(performance_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Comandos de registro separados que precisam de tratamento
            print("Ativando 'Mostrar conteúdo da janela ao arrastar'...")
            drag_command = 'Set-ItemProperty -Path "HKCU\\Control Panel\\Desktop" -Name "DragFullWindows" -Value 1 -Force'
            subprocess.run(["powershell", "-Command", drag_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            print("Ativando 'Mostrar miniaturas em vez de ícones'...")
            thumbnails_command = 'Set-ItemProperty -Path "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" -Name "IconsOnly" -Value 0 -Force'
            subprocess.run(["powershell", "-Command", thumbnails_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            print("Configuração de desempenho concluída. Algumas mudanças podem exigir uma reinicialização.")
        
        except subprocess.CalledProcessError as e:
            print(f"Ocorreu um erro ao configurar o desempenho. O script irá continuar. Detalhes: {e}")
        except Exception as e:
            print(f"Um erro inesperado ocorreu. Detalhes: {e}")

    def enable_network_sharing():
        """
        Enables network sharing for all profiles.
        """
        print("\nEnabling network sharing for all profiles...")
        try:
            # Network profiles: Domain, Private and Public
            network_profiles = ["Domain", "Private", "Public"]
            
            # Firewall rule groups to be enabled
            firewall_rules = [
                "Descoberta de Rede",
                "Compartilhamento de Arquivo e Impressora (SMB-Entrada)"
            ]
            
            for profile in network_profiles:
                for rule in firewall_rules:
                    complete_command = f'netsh advfirewall firewall set rule group="{rule}" new profile={profile} enable=yes'
                    subprocess.run(["powershell", "-Command", complete_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            print("Network sharing enabled successfully for all profiles.")
        except subprocess.CalledProcessError as e:
            print(f"Error enabling network sharing: {e}")

    def configure_sleep_time():
        """
        Configures the sleep time to 1 hour (60 minutes).
        """
        print("\nConfiguring all energy and sleep options to 1 hour (60 minutes).")
        try:
            time_in_minutes = 60  # 1 hora
            
            # Configure the screen timeout (on AC and battery)
            ac_monitor_timeout_command  = f'powercfg /change monitor-timeout-ac {time_in_minutes}'
            dc_monitor_timeout_command = f'powercfg /change monitor-timeout-dc {time_in_minutes}'
            subprocess.run(ac_monitor_timeout_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(dc_monitor_timeout_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Configure the computer standby timeout (on AC and battery)
            ac_standby_timeout_command = f'powercfg /change standby-timeout-ac {time_in_minutes}'
            dc_standby_timeout_command = f'powercfg /change standby-timeout-dc {time_in_minutes}'
            subprocess.run(ac_standby_timeout_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(dc_standby_timeout_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Configure the hibernate timeout (on AC and battery)
            ac_hibernate_timeout_command = f'powercfg /change hibernate-timeout-ac {time_in_minutes}'
            dc_hibernate_timeout_command = f'powercfg /change hibernate-timeout-dc {time_in_minutes}'
            subprocess.run(ac_hibernate_timeout_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(dc_hibernate_timeout_command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            print("All energy and sleep options adjusted to 1 hour (60 minutes).")
        except subprocess.CalledProcessError as e:
            print(f"Error adjusting energy and sleep settings: {e}")

    def configure_automatic_updates():
        """
        Configures automatic updates.
        """
        print("\nConfiguring automatic updates...")
        try:
            # Create the registry key if it doesn't exist
            create_key_command = 'New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" -Force'
            subprocess.run(["powershell", "-Command", create_key_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Set automatic updates policy to 'Automatic download and notification for installation' (value 3)
            updates_command = 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" -Name AUOptions -Value 3 -Force'
            subprocess.run(["powershell", "-Command", updates_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Automatic updates configured successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error configuring automatic updates: {e}")

    def enable_telnet_and_smb():
        """
        Enables Telnet client and SMB support.
        """
        print("\nEnabling Telnet client and SMB support...")
        try:
            # Enable Telnet client
            telnet_command = 'Enable-WindowsOptionalFeature -Online -FeatureName TelnetClient -All'
            subprocess.run(["powershell", "-Command", telnet_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Enable SMB support
            smb_command = 'Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -All'
            subprocess.run(["powershell", "-Command", smb_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            print("Telnet client and SMB support enabled successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error enabling Telnet/SMB: {e}")

    def add_users_suporte_and_administrador():
        """
        Adds the 'Suporte' and 'Administrador' users to the system.
        """
        print("--- Adding user 'Suporte' and 'Administrador' ---")
        try:
            # Read the password from the password.txt file
            with open("_private/password.txt", "r") as f:
                password = f.read().strip()

            # Add the 'suporte' user with the read password
            subprocess.run(["net", "user", "suporte", password, "/add"])

            # Add the 'administrador' user with the read password
            subprocess.run(["net", "user", "administrador", password, "/add"])

            # Add the 'suporte' user to the 'Administrators' group
            subprocess.run(["net", "localgroup", "Administradores", "suporte", "/add"])

            # Add the 'administrador' user to the 'Administrators' group
            subprocess.run(["net", "localgroup", "Administradores", "administrador", "/add"])

            print("Users 'suporte' and 'administrador' created and added to the 'Administrators' group successfully.")

        except FileNotFoundError:
            print("ERROR: The 'password.txt' file was not found. Please ensure it exists and is in the correct directory.")
        except Exception as e:
            print(f"An error occurred while adding users: {e}")
        
    def adjust_computer_name(new_name):
        """
        Adjusts the computer name.
        """
        print(f"\nAdjusting computer name to '{new_name}'...")
        try:
            name_command = f'Rename-Computer -NewName "{new_name}"'
            subprocess.run(["powershell", "-Command", name_command], check=True)
            print("Computer name changed successfully. Changes will be applied on the next restart.")
        except subprocess.CalledProcessError as e:
            print(f"Error changing computer name: {e}")

    def enable_system_protection():
        """
        Enables system protection.
        """
        print("\nEnabling system protection...")
        try:
            system_protection_command = 'Enable-ComputerRestore -Drive "C:"'
            subprocess.run(["powershell", "-Command", system_protection_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("System protection enabled successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error enabling system protection: {e}")
        
        print("Setting system restore size to 10GB...")
        try:
            system_protection_command = 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore" -Name "SRQuotaSize" -Value 10240 -Force'
            subprocess.run(["powershell", "-Command", system_protection_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("System restore size set to 10GB successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting system restore size: {e}")

    def create_system_restore_point():
        """
        Creates a system restore point.
        """
        print("\nCreating a system restore point...")
        try:
            # Command to create a system restore point with a description
            restore_point_command = 'Checkpoint-Computer -Description "System restore point before reboot"'
            subprocess.run(["powershell", "-Command", restore_point_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("System restore point created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Unable to create the system restore point. Reason: {e}")
    
    def reboot_computer():
        """
        Reinitializes the computer immediately.
        """
        answer = input("Do you want to reboot the computer? (y/n)")
        if answer == "y":
            print("Starting the computer reboot...")
            try:
                # Command to reboot the operating system.
                # The "/r" parameter means reboot, and "/t 0" means immediately.
                # The "/f" parameter forces the termination of running programs, if necessary.
                subprocess.run(["shutdown", "/r", "/t", "0", "/f"], check=True)
                print("Reboot command issued successfully.")
            except Exception as e:
                print(f"Error attempting to reboot the computer: {e}")