#!/usr/bin/env python3
import click
import os
import sys
import subprocess
import time
from pathlib import Path

@click.group()
@click.version_option("1.0", prog_name="PiFmTx-neo")
def cli():
    """
    An PiFmTx-neo CLI-tool that helps you set up and start the web server.
    """
    pass

@cli.command()
def autostart():
    service_name = "pifmtx-neo"
    script_path = f"{os.getcwd()}/main.py"
    if os.path.exists(f"/etc/systemd/system/{service_name}.service"):
        print("INFO: Already set to autostart, no need to do anything")
        print("Aborting.")
    else:
        script_path = Path(script_path).resolve()
        
        if not script_path.exists():
            print(f"ERROR: The script {script_path} does not exist.")
            return

        python_executable = sys.executable
        service_file_path = f"/etc/systemd/system/{service_name}.service"

        service_content = f"""[Unit]
        Description=PiFmtX-neo Service
        After=network.target

    [Service]
    ExecStart={python_executable} {script_path}
    WorkingDirectory={script_path.parent}
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User={os.getlogin()}

    [Install]
    WantedBy=multi-user.target
    """

        try:
            print(f"INFO: Creating service file at: {service_file_path}")
            with open("tmp_service", "w") as f:
                f.write(service_content)
    
            subprocess.run(["sudo", "mv", "tmp_service", service_file_path], check=True)
            subprocess.run(["sudo", "chown", "root:root", service_file_path], check=True)
            subprocess.run(["sudo", "chmod", "644", service_file_path], check=True)

            print("INFO: Reloading systemd daemon...")
            subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
            
            print(f"INFO: Enabling PiFmTx-neo...")
            subprocess.run(["sudo", "systemctl", "enable", service_name], check=True)
            
            print(f"INFO: Starting PiFmTx-neo...")
            subprocess.run(["sudo", "systemctl", "start", service_name], check=True)
            
            print(f"\nINFO: Successfully set up PiFmTx-neo to start on boot!")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        except PermissionError:
            print("ERROR: You need to run this script with sudo or as root.")
    
@cli.command()
def start():
    print("INFO: Starting webserver...")
    process = subprocess.Popen(["python3", "main.py"])
    
    try:
        print("INFO: Server is on.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nINFO: Stopping server...")
        process.terminate()
        process.wait()       
        print("INFO: Server stopped.")
    
if __name__ == "__main__":
    cli()