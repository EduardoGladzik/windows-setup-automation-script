import subprocess
import getpass
import os
import datetime

class SystemInformation():
    filename = "system_info.txt"
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_path = os.path.join(desktop_path, filename)

    system_informations = {
        "computer_name": subprocess.run(["wmic", "computersystem", "get", "name"], capture_output=True, text=True, check=True).stdout.strip().split()[1],
        "computer_model": subprocess.run(["wmic", "computersystem", "get", "model"], capture_output=True, text=True, check=True).stdout.strip().split()[1],
        "serial_number": subprocess.run(["wmic", "bios", "get", "serialnumber"], capture_output=True, text=True, check=True).stdout.strip().split()[1],
        "logged_user": getpass.getuser(),
        "ip_information": subprocess.run(["ipconfig"], capture_output=True, text=True, check=True).stdout
    }


    def write_information(file, info, data):
        """
        Export system information to "system_info.txt".
        """
        try:
            file.write(f"--- {info.replace('_', ' ').title()} ---\n")
            file.write(f"{data}\n\n")
        except Exception as e:
            print(f"Erro ao escrever informações: {e}")
            return
        
    def create_system_info_file(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            try:
                file.write("### Relatório de Informações do Sistema ###\n\n")
                file.write(f"Data e Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                for info, data in self.system_informations.items():
                    self.write_information(file, info, data)
                print(f"Informações do sistema exportadas para {self.filename}!")
            except Exception as e:
                print(f"Erro ao criar o arquivo '{self.filename}': {e}")