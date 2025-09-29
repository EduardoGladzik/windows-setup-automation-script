import subprocess

class WindowsConfiguration():
    time_in_minutes = 60
    commands = {
        "ac_monitor_timeout": f'powercfg /change monitor-timeout-ac {time_in_minutes}',
        "dc_monitor_timeout": f'powercfg /change monitor-timeout-dc {time_in_minutes}',
        "ac_standby_timeout": f'powercfg /change standby-timeout-ac {time_in_minutes}',
        "dc_standby_timeout": f'powercfg /change standby-timeout-dc {time_in_minutes}',
        "ac_hibernate_timeout": f'powercfg /change hibernate-timeout-ac {time_in_minutes}',
        "dc_hibernate_timeout": f'powercfg /change hibernate-timeout-dc {time_in_minutes}',
    }


    def disable_uac():
        """
        Disables User Account Control (UAC).
        """
        try:
            uac_command = 'Set-ItemProperty -Path "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "EnableLUA" -Value 0 -Force'
            subprocess.run(["powershell", "-Command", uac_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("UAC desabilitado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao desabilitar UAC: {e}")
    

    def enable_rdp():
        """
        Enables Remote Desktop Connection.
        """
        try:
            rdp_command = 'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" -Name "fDenyTSConnections" -Value 0 -Force'
            subprocess.run(["powershell", "-Command", rdp_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Conexão com Área de Trabalho Remota habilitada com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao habilitar Conexão com Área de Trabalho Remota: {e}")


    def enable_network_sharing():
        """
        Enables network sharing for all profiles.
        """
        print("\nHabilitando compartilhamento de rede para todos os perfis...")
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
                    command = f'netsh advfirewall firewall set rule group="{rule}" new profile={profile} enable=yes'
                    subprocess.run(["powershell", "-Command", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            print("Compartilhamento de rede habilitado com sucesso para todos os perfis.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao habilitar compartilhamento de rede: {e}")


    def configure_sleep_time(self):
        """
        Configures the sleep time to 1 hour.
        """
        try:
            for command in self.commands.values():
                subprocess.run(command.split(), check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            print("Todas as opções de energia e suspensão ajustadas para 1 hora.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao ajustar configurações de energia e suspensão: {e}")


    def configure_automatic_updates():
        """
        Configures automatic updates for Windows 11.
        Requires administrator privileges.
        """
        print("\nConfigurando atualizações automáticas...")
        try:
            # Define the registry paths
            au_path = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU"
            wu_path = "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate"

            commands = [
                f'New-Item -Path "{wu_path}" -Force',
                f'New-Item -Path "{au_path}" -Force',
                # Enable Automatic Updates
                f'Set-ItemProperty -Path "{au_path}" -Name "NoAutoUpdate" -Value 0 -Type DWord -Force',
                # Configure auto download and notify for install (3 = Auto download and notify for install)
                f'Set-ItemProperty -Path "{au_path}" -Name "AUOptions" -Value 3 -Type DWord -Force',
                # Enable automatic updates
                f'Set-ItemProperty -Path "{au_path}" -Name "UseWUServer" -Value 0 -Type DWord -Force',
                # Configure update detection frequency
                f'Set-ItemProperty -Path "{au_path}" -Name "DetectionFrequencyEnabled" -Value 1 -Type DWord -Force',
                f'Set-ItemProperty -Path "{au_path}" -Name "DetectionFrequency" -Value 22 -Type DWord -Force',
                # Windows 11 specific settings
                f'Set-ItemProperty -Path "{wu_path}" -Name "TargetReleaseVersion" -Value 1 -Type DWord -Force',
                f'Set-ItemProperty -Path "{wu_path}" -Name "DisableWUfBSafeguards" -Value 0 -Type DWord -Force'
            ]

            for command in commands:
                subprocess.run(["powershell", "-Command", command], 
                            check=True, 
                            creationflags=subprocess.CREATE_NO_WINDOW)

            print("Atualizações automáticas configuradas com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao configurar atualizações automáticas: {e}")
            print("Certifique-se de executar o script como administrador.")


    def enable_telnet_and_smb():
         """
         Enables Telnet client and SMB support.
         """
         try:
             telnet_command = 'Enable-WindowsOptionalFeature -Online -FeatureName TelnetClient -All'
             subprocess.run(["powershell", "-Command", telnet_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
             smb_command = 'Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -All'
             subprocess.run(["powershell", "-Command", smb_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

             print("Cliente Telnet e suporte SMB habilitados com sucesso.")
         except subprocess.CalledProcessError as e:
             print(f"Erro ao habilitar Telnet/SMB: {e}")


    def alter_computer_name(new_name):
        """
        Adjusts the computer name.
        """
        try:
            alter_computer_name_command = f'Rename-Computer -NewName "{new_name}"'
            subprocess.run(["powershell", "-Command", alter_computer_name_command], check=True)
            print("Nome do computador alterado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao alterar nome do computador: {e}")


    def enable_system_protection():
        """
        Enables system protection.
        """
        try:
            enable_system_protection_command = 'Enable-ComputerRestore -Drive "C:"'
            subprocess.run(["powershell", "-Command", enable_system_protection_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Proteção do sistema habilitada com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao habilitar proteção do sistema: {e}")
        
        print("Definindo tamanho do ponto de restauração para 10GB...")
        try:
            set_system_restore_size_command = 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SystemRestore" -Name "SRQuotaSize" -Value 10240 -Force'
            subprocess.run(["powershell", "-Command", set_system_restore_size_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Tamanho do ponto de restauração definido para 10GB com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao definir tamanho do ponto de restauração: {e}")


    def create_system_restore_point():
        """
        Creates a system restore point.
        """
        try:
            create_system_restore_point_command = 'Checkpoint-Computer -Description "System restore point before reboot"'
            subprocess.run(["powershell", "-Command", create_system_restore_point_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Ponto de restauração do sistema criado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao criar ponto de restauração do sistema: {e}")
    

    def reboot_computer():
        """
        Reinitializes the computer immediately.
        """
        try:
            # The "/r" parameter means reboot
            # The "/f" parameter forces the termination of running programs, if necessary.
            subprocess.run(["shutdown", "/r", "/f", "/s"], check=True)
            print("Comando de reinicialização executado com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar reinicializar o computador: {e}")