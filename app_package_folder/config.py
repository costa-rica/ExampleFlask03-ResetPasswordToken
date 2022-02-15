import os#<---Here config.json
import json#<--- Here config.json

if os.environ.get('COMPUTERNAME')=='CAPTAIN2020':#<--- Here config.json
    with open(r'C:\Users\captian2020\Documents\config_files\config_kmUploaderV4.json') as config_file:#<--- Here config.json
        config = json.load(config_file)#<--- Here config.json

class Config:
    DEBUG = True
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///exampleFlask02.db'
    # MAIL_SERVER = 'smtp.googlemail.com'#<---Here
    MAIL_SERVER = config.get('MAIL_SERVER_MSOFFICE')
    MAIL_PORT = 587#<---Here
    MAIL_USE_TLS = True#<---Here
    MAIL_USERNAME = config.get('MAIL_EMAIL_DD')#<---Here
    MAIL_PASSWORD = config.get('MAIL_PASSWORD_DD')#<---Here