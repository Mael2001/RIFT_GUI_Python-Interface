import ftplib
import os
import urllib.request
import re

ftpCredential = {
    'host_name': 'ftpupload.net',
    'user_name': 'lblog_32136658',
    'user_password' : 'tfdg4k'
}

def downloadFTP():
    session = ftplib.FTP(ftpCredential['host_name'],ftpCredential['user_name'],ftpCredential['user_password'])
    basePath = "./FTP"
    FTPfoldersToDownload = ['images','videos']

    if not os.path.exists(basePath):
        os.mkdir(basePath)
    for folder in FTPfoldersToDownload:
        if not os.path.exists(f'{basePath}/{folder}'):
            os.mkdir(f'{basePath}/{folder}')
        for item in session.nlst(f'./{folder}'):
            if item == '.' or item == '..':
                continue
            print(f'Downloading {item}')
            urllib.request.urlretrieve(f'ftp://{ftpCredential["user_name"]}:{ftpCredential["user_password"]}@{ftpCredential["host_name"]}/{folder}/{item}', f'./FTP/{folder}/{item}')
    session.close()

if __name__ == "__main__":
    downloadFTP()