from modules.information import gather_and_export_information
from modules.instalation import install_softwares
from modules.windows import WindowsConfiguration

def main():
    gather_and_export_information()
    install_softwares()
    WindowsConfiguration.disable_uac()
    WindowsConfiguration.enable_rdp()
    WindowsConfiguration.adjust_performance_settings()
    WindowsConfiguration.enable_network_sharing()
    WindowsConfiguration.configure_sleep_time()
    WindowsConfiguration.configure_automatic_updates()
    WindowsConfiguration.enable_telnet_and_smb()
    WindowsConfiguration.add_users_suporte_and_administrador()
    WindowsConfiguration.adjust_computer_name(input("Enter the new computer name: "))
    WindowsConfiguration.enable_system_protection()
    WindowsConfiguration.create_system_restore_point()
    WindowsConfiguration.reboot_computer()

if __name__ == "__main__":
    main()