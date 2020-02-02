# Twilio Phone Number Manager

A set of tools to manager alternate Twilio number and to connect it with a current number

## Terminal Set Up

To use from the terminal, download repository and enter the following into your bash
aliases: `alias sms=python3 <DIRECTORY>/Twilio_Redirect/main.py`
This will allow you to type `sms` from any directory to call main.py

Additionally, you will need to configure a .env file in `<DIRECTORY>` that will contain the following variables:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_ACCOUNT_TOKEN`
- `TWILIO_NUMBER`
- `TWILIO_REGION_CODE`
- `TARGET_NUMBER`
- `TARGET_REGION_CODE`
- `PATH`

## Terminal Use / Commands

Arguments passable to main.py

- ` ` : will display all new texts
- `Hello World` : will send message 'Hello World' to default target phone number
- `1234567890 Hello World` : will send message 'Hello World' to number '+1 (123) 456 7890'
- `+11234567890 Hello World` : will send message 'Hello World' to number '+1 (123) 456 7890'

