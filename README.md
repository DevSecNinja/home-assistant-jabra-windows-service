## Create a secrets.ini in the root containing:
[DEFAULT]
HomeAssistantURL = https://<HomeAssistantUrl>/api/states/sensor.jabraheadset
HomeAssistantAuth = Bearer <Long Lived Access Token>

Tip: you can rename the `secrets.ini.example` file to `secrets.ini`.

## Run the Python script as service
python .\main.py --startup auto --wait 2 install

## If you want to debug the script
python .\main.py --startup auto --wait 2 debug