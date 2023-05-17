# AI helps PWR
Repository for [Hack4WroclawTech](https://hack4wroclawtech.my.canva.site/) hackhaton with project which will improve 
working at Wroclaw University of Science and Technology applying some AI solution.

**Our idea: Dean office assistant**

It automatically responds for students mails.

## Installation
Required:
 - python 3.9
 - [poetry](https://python-poetry.org/)

The project uses [poetry](https://python-poetry.org/) tool. So you should have it preinstalled

```bash
poetry install  # create venv and install all dependencies
poetry shell  # activate venv
```

## Configuration

### Use GPT
You should copy the config file from `config/config` to `config/config.local` and complete with your key.
```
[eventRegistry]
apiKey = yourapiKey
```
Then you can use:
```
experiments/scripts/conversation.py
```
where example input prompt you can find in `data/test_prompt.json`

### Sending email
To send email please add to config.local file:
```
[email]
sender = yourmail
password = yourpassword
```

Under the link please find how to get password: https://support.google.com/accounts/answer/185833?hl=pl, 
and create new app_password: https://myaccount.google.com/u/1/apppasswords.

## Running demo
```
demo_app
```
It should run streamlit app and open it in a browser. 

There you can type student email for which will be generated autoresponse.
