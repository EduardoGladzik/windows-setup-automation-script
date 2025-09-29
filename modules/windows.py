import subprocess

class WindowsConfiguration():

    def disable_uac():
        """
        Disables User Account Control (UAC).
        """
        print("--- Desabilitando o Controle de Conta de Usuário (UAC) ---")
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
        print("\n--- Habilitando Conexão com Área de Trabalho Remota ---")
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


    def configure_sleep_time():
        """
        Configures the sleep time to 1 hour (60 minutes).
        """
        print("\nConfigurando todas as opções de energia e suspensão para 1 hora.")
        try:
            time_in_minutes = 60
            
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
            
            print("Todas as opções de energia e suspensão ajustadas para 1 hora.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao ajustar configurações de energia e suspensão: {e}")


    def configure_automatic_updates():
        """
        Configures automatic updates.

        """
        print("\nConfigurando atualizações automáticas...")
        try:
            # Create the registry key if it doesn't exist
            create_key_command = 'New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" -Force'
            subprocess.run(["powershell", "-Command", create_key_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            # Set automatic updates policy to 'Automatic download and notification for installation' (value 3)
            updates_command = 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" -Name AUOptions -Value 3 -Force'
            subprocess.run(["powershell", "-Command", updates_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Atualizações automáticas configuradas com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao configurar atualizações automáticas: {e}")


    def enable_telnet_and_smb():
         """
         Enables Telnet client and SMB support.
         """
         print("\nHabilitando cliente Telnet e suporte SMB...")
         try:
             # Enable Telnet client
             telnet_command = 'Enable-WindowsOptionalFeature -Online -FeatureName TelnetClient -All'
             subprocess.run(["powershell", "-Command", telnet_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
             # Enable SMB support
             smb_command = 'Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -All'
             subprocess.run(["powershell", "-Command", smb_command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

             print("Cliente Telnet e suporte SMB habilitados com sucesso.")
         except subprocess.CalledProcessError as e:
             print(f"Erro ao habilitar Telnet/SMB: {e}")


    def add_users_suporte_and_administrador():
        """
        Adds the 'Suporte' and 'Administrador' users to the system.
        """
        print("--- Adicionando usuário 'Suporte' e 'Administrador' ---")
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

            print("Usuários 'suporte' e 'administrador' criados e adicionados ao grupo 'Administradores' com sucesso.")

        except FileNotFoundError:
            print("ERRO: O arquivo 'password.txt' não foi encontrado. Certifique-se de que ele existe e está no diretório correto.")
        except Exception as e:
            print(f"Ocorreu um erro ao adicionar usuários: {e}")


    def alter_computer_name(new_name):
        """
        Adjusts the computer name.
        """
        try:
            adjust_computer_name_command = f'Rename-Computer -NewName "{new_name}"'
            subprocess.run(["powershell", "-Command", adjust_computer_name_command], check=True)
            print("Nome do computador alterado com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao alterar nome do computador: {e}")


    def enable_system_protection():
        """
        Enables system protection.
        """
        print("\nHabilitando proteção do sistema...")
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
        print("\nCriando ponto de restauração do sistema...")
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