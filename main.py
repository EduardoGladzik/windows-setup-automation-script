import subprocess
from modules.information import SystemInformation as sysinfo
from modules.softwares import Softwares as softwares
from modules.windows import WindowsConfiguration as winconfig
import os


def main():
    
    print(" ========================================="
          + "\nIniciando Script de Configuração do Windows"
          + "\n =========================================")
    
    print("\n--- Informações do sistema ---")
    print("coletando informações do sistema...")
    print(f"criando {sysinfo.filename} na área de trabalho...")
    if not os.path.exists(sysinfo.file_path):
        sysinfo.create_system_info_file(sysinfo)
    else:
        print(f"O arquivo '{sysinfo.filename}' já existe na área de trabalho.")

    print("\n--- Instalação de Softwares ---")
    for name, data in softwares.software_list.items():
        if softwares.is_installed(data["verification_name"]):
            print(f"\n{name} já está instalado. Pulando instalação.")
            continue
       
        if not os.path.exists(data["local_path"]):
            print(f"\nArquivo de instalação para {name} não encontrado. Pulando instalação.")
            continue
        
        print("--- Iniciando instalação dos softwares a partir dos arquivos locais ---")
        print(f"\nIniciando instalação de {name}...")
        softwares.install_softwares(name, data)

    print("\n--- Desabilitando o Controle de Conta de Usuário (UAC) ---")
    winconfig.disable_uac()

    print("\n--- Habilitando Conexão com Área de Trabalho Remota ---")
    winconfig.enable_rdp()

    print("\n--- Configurações de Desempenho ---")
    print("\nAlterando configurações...")
    winconfig.configure_performance_settings()

    print("\n--- Configurando Atualizações Automáticas ---")
    # winconfig.configure_automatic_updates()

    print("\n--- Habilitando Telnet e SMB ---")
    print("\nHabilitando cliente Telnet e suporte SMB...")
    winconfig.enable_telnet_and_smb()

    print("\n--- Configurações de Rede ---")
    print("\nHabilitando compartilhamento de rede...")
    winconfig.enable_firewall_group_rules(winconfig)

    print("\n--- Configurações de Energia ---")
    print("\nConfigurando todas as opções de energia e suspensão para 1 hora.")
    winconfig.configure_sleep_time(winconfig)

    print("\n--- Configuração do Nome do Computador ---")
    print(f"Nome atual do computador: {os.environ['COMPUTERNAME']}")
    new_computer_name = input("\nDigite o novo nome do computador ou pressione Enter para manter o nome atual: ")
    if not new_computer_name:
        print("Nome do computador não alterado.")

    else:
        print(f"\nAlterando nome do computador para '{new_computer_name}'...")
        winconfig.alter_computer_name()
    
    print("\n--- Configurações de Backup e Restauração ---")
    print("\nHabilitando proteção do sistema...")
    winconfig.enable_system_protection()

    print("\nCriando ponto de restauração do sistema...")
    winconfig.create_system_restore_point()
    
    print("\n--- Finalizando Script ---")
    answer = input("Digite 's' para reiniciar o computador enter para finalizar o script: ")
    if answer.lower() == 's':
        winconfig.reboot_computer()
    elif not answer or answer.lower() != 's':
        print("Script executado com sucesso!\nAlgumas alterações serão aplicadas após reinicialização.")

if __name__ == "__main__":
    subprocess.run(["cls"], shell=True)
    main()