import subprocess
import getpass
import datetime
import os

def gather_and_export_information():
    # Define the filename with date and time to avoid overwriting
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"system_info_{date_time}.txt"

    # Get the current user's desktop path
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    full_path = os.path.join(desktop_path, filename)

    print(f"--- Exportando informações para o arquivo '{full_path}' ---")

    # Open the file in write mode ('w') on the desktop path
    with open(full_path, "w", encoding="utf-8") as file:
        # Title
        file.write("### Relatório de Informações do Sistema ###\n\n")
        file.write(f"Data e Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        # Computer name
        file.write("1. Nome do computador: ")
        try:
            computer_name = subprocess.run(["wmic", "computersystem", "get", "name"], capture_output=True, text=True, check=True)
            file.write(f"{computer_name.stdout.strip().split()[1]}\n\n")
        except subprocess.CalledProcessError as e:
            file.write(f"Erro ao executar comando: {e}\n\n")

        # Computer model
        file.write("2. Modelo do computador: ")
        try:
            computer_model = subprocess.run(["wmic", "computersystem", "get", "model"], capture_output=True, text=True, check=True)
            file.write(f"{computer_model.stdout.strip().split()[1]}\n\n")
        except subprocess.CalledProcessError as e:
            file.write(f"Erro ao executar comando: {e}\n\n")

        # Serial number
        file.write("3. Número de série: ")
        try:
            serial_number = subprocess.run(["wmic", "bios", "get", "serialnumber"], capture_output=True, text=True, check=True)
            file.write(f"{serial_number.stdout.strip().split()[1]}\n\n")
        except subprocess.CalledProcessError as e:
            file.write(f"   Erro ao executar comando: {e}\n\n")

        # Logged user
        file.write("4. Usuário logado: ")
        file.write(f"   {getpass.getuser()}\n\n")

        # IP information
        file.write("5. Informações de IP:\n")
        try:
            result = subprocess.run(["ipconfig"], capture_output=True, text=True, check=True)
            file.write(result.stdout + "\n")
        except subprocess.CalledProcessError as e:
            file.write(f"   Erro ao executar comando: {e}\n\n")

    print(f"Exportação concluída! Verifique o arquivo '{full_path}'.")