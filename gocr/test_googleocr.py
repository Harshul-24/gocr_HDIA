from __future__ import print_function
import httplib2
import os
import io
import numpy as np
import pandas as pd
import six
import sys
from googleapiclient import errors  #pip install --upgrade google-api-python-client
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
# try:
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/drive'
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = r'C:/Users/User/Documents/IHDIA_cloud_vision/gocr/client_secrets.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
if len(sys.argv)<2:
    sys.exit("Format: python model/google_ocr/test_googleocr.py <path_to_test_file>")

path_to_testfile = sys.argv[1]
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # SCOPES = ['https://www.googleapis.com/auth/drive.appdata']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(host='localhost', port=8080)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main():
    credentials = get_credentials()
    # http = credentials.authorize(httplib2.Http())
    service = build('drive', 'v3', credentials=credentials)
    ct = 0
    l=0
    if not os.path.exists(os.getcwd()+"/result"):
        os.mkdir(os.getcwd()+"/result")
    with open(os.getcwd()+'/'+path_to_testfile,'r',encoding="utf8", errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            loc = line.strip()

            imgfile = loc
            txtfile = os.getcwd()+'/result/'+str(ct)+'.txt'
            
            if os.path.exists(txtfile)==False:
                mime = 'application/vnd.google-apps.document'
                res = service.files().create(
                    body={
                        'name': imgfile,
                        'mimeType': mime
                    },
                    media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
                ).execute()

                downloader = MediaIoBaseDownload(
                    io.FileIO(txtfile, 'wb'),
                    service.files().export_media(fileId=res['id'], mimeType="text/plain")
                )

                done = False
                try:
                    while done is False:
                        status, done = downloader.next_chunk()

                    service.files().delete(fileId=res['id']).execute()
                    print("Done")
                except:
                    print('ERROR!')
            else:
                with open(txtfile) as fx:
                    l = fx.readlines()
                if len(l)<3:
                    mime = 'application/vnd.google-apps.document'
                    res = service.files().create(
                        body={
                            'name': imgfile,
                            'mimeType': mime
                        },
                        media_body=MediaFileUpload(imgfile, mimetype=mime, resumable=True)
                    ).execute()

                    downloader = MediaIoBaseDownload(
                        io.FileIO(txtfile, 'wb'),
                        service.files().export_media(fileId=res['id'], mimeType="text/plain")
                    )

                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()

                    service.files().delete(fileId=res['id']).execute()
                    print("Done")

            ct = ct+1
            print(ct)
            
                # file_handle = io.BytesIO()
                # downloader = MediaIoBaseDownload(
                #     file_handle,
                #     service.files().export_media(fileId=res['id'], mimeType="text/plain")
                # )
                # done = False
                # while done is False:
                #     status, done = downloader.next_chunk()
                # filevalue = file_handle.getvalue()
                # if not isinstance(filevalue, six.string_types):
                #     filevalue = filevalue.decode('UTF-8')
                
                # print(filevalue[21:])
                # pred_gocr.append(filevalue[21:])
                # service.files().delete(fileId=res['id']).execute()
                # # output = six.StringIO(filevalue)

                # print("Done.")


if __name__ == '__main__':
    main()