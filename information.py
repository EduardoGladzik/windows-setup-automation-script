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

    print(f"--- Exporting information to file '{full_path}' ---")

    # Open the file in write mode ('w') on the desktop path
    with open(full_path, "w", encoding="utf-8") as file:
        # Title
        file.write("### System Information Report ###\n\n")
        file.write(f"Date and Time: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        # Computer name
        file.write("1. Computer name: ")
        try:
            computer_name = subprocess.run(["wmic", "computersystem", "get", "name"], capture_output=True, text=True, check=True)
            file.write(f"{computer_name.stdout.strip().split()[1]}\n\n")
        except subprocess.CalledProcessError as e:
            file.write(f"Error executing command: {e}\n\n")

        # Computer model
        file.write("2. Computer model: ")
        try:
            computer_model = subprocess.run(["wmic", "computersystem", "get", "model"], capture_output=True, text=True, check=True)
            file.write(f"{computer_model.stdout.strip().split()[1]}\n\n")
        except subprocess.CalledProcessError as e:
            file.write(f"Error executing command: {e}\n\n")

        # Serial number
        file.write("3. Serial number: ")
        try:
            serial_number = subprocess.run(["wmic", "bios", "get", "serialnumber"], capture_output=True, text=True, check=True)
            file.write(f"{serial_number.stdout.strip().split()[1]}\n\n")
        except subprocess.CalledProcessError as e:
            file.write(f"   Error executing command: {e}\n\n")

        # Logged user
        file.write("4. Logged user: ")
        file.write(f"   {getpass.getuser()}\n\n")

        # IP information
        file.write("5. IP information:\n")
        try:
            result = subprocess.run(["ipconfig"], capture_output=True, text=True, check=True)
            file.write(result.stdout + "\n")
        except subprocess.CalledProcessError as e:
            file.write(f"   Error executing command: {e}\n\n")

    print(f"Export completed! Check the file '{full_path}'.")