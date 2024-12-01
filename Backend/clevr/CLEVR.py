import requests
import Backend.config as conf
from requests.auth import HTTPBasicAuth
import time


baseurl = conf.url_clevr
# The date needs to be in the following format: 2021-12-13T20:38:51.343Z
# or just use the year,month and day 2021-12-13

# try timeout times until break out
timeout = 5

def get_data_dump(error_counter=0):
    url = baseurl

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
    response = requests.get(url, auth=HTTPBasicAuth('DownloadUser', 'g3pUzGor%S^5'), headers=headers, timeout=8)
    print("[DATA DUMP] Status response from CLEVR backend: "+ str(response))

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 408:
        print("no internet... try local")
    elif error_counter <= 5:
        time.sleep(1)
        get_data_dump(error_counter=error_counter+1)
    else:
        return {}


def get_data_since_date(date, error_counter=0):
    if date == "":
        url = baseurl + "files"
    else:
        url = baseurl + "files?createdAfter={}".format(date)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
    response = requests.get(url, auth=HTTPBasicAuth('DownloadUser', 'g3pUzGor%S^5'), headers=headers, timeout=8)
    print("[SINCE DATE] Status response from CLEVR backend: "+ str(response))

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 408:
        print("no internet... try local")
    elif error_counter <= 5:
        time.sleep(1)
        get_data_since_date(date, error_counter=error_counter+1)
    else:
        return {}


def get_all_data(error_counter=0):
    url = baseurl + "allfiles"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
    response = requests.get(url, auth=HTTPBasicAuth('DownloadUser', 'g3pUzGor%S^5'), headers=headers, timeout=8)
    print("[ALL DATA] Status response from CLEVR backend: "+ str(response))
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 408:
        print("no internet... try local")
    elif error_counter <= 5:
        time.sleep(1)
        get_all_data(error_counter=error_counter+1)
    else:
        return {}


def send_recommendation(json, error_counter=0):
    url = "https://guideexport-sandbox.mxapps.io/rest/upload/v1/recommendation"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
    response = requests.post(url, auth=HTTPBasicAuth('DownloadUser', 'g3pUzGor%S^5'), json=json, headers=headers, timeout=8)
    print("[RECOMMENDATION] Status send response to CLEVR backend: "+ str(response))

    if response.status_code == 200:
        return {}
    elif response.status_code == 408:
        print("no internet... try local")
    elif error_counter <= 5:
        time.sleep(1)
        send_recommendation(json, error_counter=error_counter+1)
    else:
        return {}


def get_data_uuid(uuid, error_counter=0):
    url = baseurl + "file?UUID={}".format(uuid)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
    response = requests.get(url, auth=HTTPBasicAuth('DownloadUser', 'g3pUzGor%S^5'),  headers=headers, timeout=8)
    print("[GET UUID] Status response from CLEVR backend: "+ str(response))
    # add timeout status code and timeout of 5-10 sec
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 408:
        print("no internet... try local")
    elif error_counter <= 5:
        time.sleep(1)
        get_data_uuid(uuid, error_counter=error_counter+1)
    else:
        return {}
