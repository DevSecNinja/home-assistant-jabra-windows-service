# Home Assistant Jabra Windows Service

Welcome! This Python based Windows Service communicates the status of your Jabra headset to Home Assistant.

## Requirements
- Python 3.* installed and added to PATH

## How to install
- Open a PowerShell window as administrator and run:

```` powershell
pip install -r .\requirements.txt
````
Make sure that the packages show up under `C:\Program Files (x86)\Python*\Lib\site-packages` as the Windows Service needs to access it.

- Run the ![postinstall.py](https://github.com/mhammond/pywin32/blob/master/pywin32_postinstall.py) script from the PowerShell console with administrator privileges.

- Clone or download the source code from this repository. Copy `secrets.example.ini` to `secrets.ini` and provide the required info.

- Make sure the `SYSTEM` account has access to this folder as the service will run under `SYSTEM`.

- Browse to the location and run the code below in PowerShell with administrator privileges:

```` powershell
python .\main.py --startup auto --wait 2 install
python .\main.py start
````

## Troubleshooting
- Check if the service is started. In PowerShell, run:
```` powershell
Get-Service -Name "JabraHomeAssistantSync"
Get-Service -Name "JabraHomeAssistantSync" | Start-Service
````

- You can run the following code to debug the service:

```` powershell
python .\main.py debug
````

- In case you receive the error `Error starting service: The service did not respond to the start or control request in a timely fashion` during the start of the service,
make sure to have the `pywintypes36.dll` file available from the `C:\Program Files (x86)\Python*\Lib\site-packages\win32` folder. In case the file is missing,
copy it from the `C:\Program Files (x86)\Python*\Lib\site-packages\pywin32_system32` folder.
- Open up an issue within this repository in case your issue is not listed here or listed as a closed issue.
