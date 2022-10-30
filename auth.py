

from ast import Starred
from http import server





from pip import main
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive




def ferst_auth():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    # View all folders and file in your Google Drive
    return drive


import json
import re
from warnings import catch_warnings
from requests import request
from Gooogle import Create_Service 



def second_auth ():
    Client_secret = 'client_secret.json'
    Api_Name='drive'
    Api_version = 'v3'
    Scoop = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(Client_secret,Api_Name,Api_version,Scoop)
    return service


