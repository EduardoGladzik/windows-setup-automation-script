import subprocess
import os

def check_and_install_updates():
    print("--- Iniciando o módulo de atualização ---")

    # 1. Atualizar o Windows Update
    print("\nVerificando e instalando atualizações do Windows...")
    try:
        comando_updates = 'Install-Module PSWindowsUpdate -Force -SkipPublisherCheck -Confirm:$false; Get-WUInstall -MicrosoftUpdate -AcceptAll -AutoReboot'
        subprocess.run(["powershell", "-Command", comando_updates], check=True)
        print("Atualizações do Windows instaladas com sucesso. O sistema pode ser reiniciado se necessário.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar o Windows: {e}")

    # 2. Atualizar o Gerenciador de Pacotes do Windows (winget)
    print("\nVerificando e instalando atualizações de softwares com o winget...")
    try:
        # Comando para listar todas as atualizações disponíveis e instalá-las
        comando_winget_upgrade = "winget upgrade --all --silent --accept-package-agreements --accept-source-agreements"
        subprocess.run(comando_winget_upgrade.split(), check=True)
        print("Atualizações de softwares via winget concluídas.")
    except FileNotFoundError:
        print("Aviso: 'winget' não foi encontrado. O Gerenciador de Pacotes do Windows não está instalado ou não está no PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar softwares com winget: {e}")

    # --- NOVA FUNCIONALIDADE: ATUALIZAÇÃO DE DRIVERS ---
    
    # 3. Verificar e atualizar drivers com winget
    print("\nVerificando e atualizando drivers de sistema...")
    try:
        # O winget trata os drivers como pacotes a serem atualizados.
        # O comando abaixo verifica todos os pacotes instalados
        # e tenta atualizar aqueles para os quais há uma versão mais recente,
        # incluindo drivers de hardware.
        comando_drivers = "winget upgrade --include-unknown --all --silent --accept-package-agreements --accept-source-agreements"
        subprocess.run(comando_drivers.split(), check=True)
        print("Verificação e atualização de drivers concluída com sucesso.")

    except subprocess.CalledProcessError as e:
        print(f"Aviso: Não foi possível atualizar todos os drivers automaticamente. Motivo: {e}. Verifique as atualizações manualmente no Gerenciador de Dispositivos ou no site do fabricante.")
    except FileNotFoundError:
        print("Aviso: 'winget' não foi encontrado. Não foi possível verificar os drivers.")

    print("\n--- Módulo de atualização concluído ---")