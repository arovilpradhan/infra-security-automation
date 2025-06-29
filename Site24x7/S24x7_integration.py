# This Script is used to communicate with Site24x7 portal using API and perform actions as per requirement.
# Specifically in this script first we got the API Key refreshing code and use the API/refresh key/token to find a monitor's ID First 
# when given as input and then delete that same monitor from the Site24x7 portal and acknowledge same to user.
import json
import os
import urllib.request
import urllib.parse
import requests
from flask import Flask, request, jsonify

"""
Fill in the Client ID , Client Secret and the generated code (Self Client). Visit https://api-console.zoho.com to create one.
The getAccessTokenMethod() should be sufficient for most of the use cases. It generates the access_token and refresh_token from the generated code for the first time. Then it uses the refresh token to automatically refresh and return the updated access_token.
If you want the access token in the accepted header format use the getAccessTokenWithHeader() method. 
"""

#Client Details
client_id="1000.DMGJ9AK70W5dsfsdfxxxxx5KP0RIFR8JP2Z"
client_secret="043f23229fffbdsfsfsdfsdxxxxx3455971ff2fc026"
code="1000.46d9e118axcxxxxxxxa04733e1e5484.c4e6bc19sdfsdfsdfsf03820f49dda"

url="https://accounts.zoho.com/oauth/v2/token"
datetime_format="%Y-%m-%d %H:%M:%S.%f"
lastGeneratedOauth={}
header={"Accept":"application/json; version=2.1"}

PATH=""
CLIENT_FILE="Site24x7OauthTokenDetails.json" # This file will be used for storing the generated token.

ENCODING="utf-8"
READ="r"
WRITE="w"

AUTHORIZATION="Authorization"
AUTHORIZATION_CODE="authorization_code"
ACCESS_TOKEN="access_token"
CLIENT_ID="client_id"
CLIENT_SECRET="client_secret"
ERROR_CODE="error_code"
ERROR="error"
EXPIRES_IN="expires_in_sec"
GRANT_TOKEN="code"
GRANT_TYPE="grant_type"
REFRESH_TOKEN="refresh_token"
VALID_UNTIL="valid_until"
TOKEN_PREFIX="Zoho-oauthtoken "

message_NO_DIRECTORY="Creating directory 'data'.\nAll Client information for generating oauth will be stored under this directory in "
message_PERIOD=" ."
message_NO_EXISTING_OAUTH="No existing OAuthTokens found."
message_FILE_WRITE_EXCEPTION="Error while writing to file "
message_OAUTH_ACCESS_TOKEN_ERROR="Error while generating OAuth Access Token ."
message_REFRESH_TOKEN_ERROR="Error Occurred while trying to refresh token ."
message_NO_FILE="ClientFile not found ."
message_CONNECTION="Error while making Connection ."



def writeToFile(path=None,data=None):
    try:
        if data is not None:
            with open(path, WRITE, encoding=ENCODING) as f:
                json.dump(data,f,sort_keys=True, indent=2,default=str)
    except:
        print(message_FILE_WRITE_EXCEPTION+path+message_PERIOD)
        


def readFromFile(path=None):
    try:
        with open(path, READ, encoding=ENCODING) as f:
            data = json.load(f)
        return data

    except:
        print(message_NO_FILE)
        return None

def encodeQueryParams(url,params):
    if params is not None:
        from urllib.parse import urlencode
        return url + "?" + urlencode(params)
    else:
        return url

def makeRequest(requestType,url,data=None,header=None,params=None):
    try:

        if requestType == "GET":
            request = urllib.request.Request(url,headers=header)
            response = urllib.request.urlopen(request).read()
            return response
        elif requestType == "POST":
            url = encodeQueryParams(url,params)
            data = data.encode(ENCODING) if data is not None else None
            params=json.dumps(params)
            params = params.encode(ENCODING) if params is not None else None

            if header is not None:
                request = urllib.request.Request(url,data=data,headers=header)
            else:
                request = urllib.request.Request(url,params)

            response = urllib.request.urlopen(request).read()
            return response
    except:
        print(message_CONNECTION)

def generateAccessToken():
#This method generates the access_token and refresh token from the client_id, client_secret and code provided. 
    try:

        params={
            CLIENT_ID:client_id,
            CLIENT_SECRET:client_secret,
            GRANT_TOKEN:code,
            GRANT_TYPE:AUTHORIZATION_CODE
        }

        response=makeRequest("POST",url,params=params)
        decodedResponseData = json.loads(response.decode(ENCODING))

        if ERROR_CODE and ERROR not in decodedResponseData:
            from datetime import datetime,timedelta
            now = datetime.now()
            EXPIRES_IN="expires_in" if "expires_in_sec" not in decodedResponseData else "expires_in_sec"
            decodedResponseData[VALID_UNTIL]=now+timedelta(seconds=decodedResponseData[EXPIRES_IN])
            writeToFile(os.path.join(PATH,CLIENT_FILE),decodedResponseData)
        else:
            print(message_OAUTH_ACCESS_TOKEN_ERROR)
            print(decodedResponseData)

    except Exception as e:
        print(decodedResponseData)
        print(e.__class__,e.args)

def refreshAccessToken():
# This method refreshes the access_token.
    try:

        params={
            CLIENT_ID:client_id,
            CLIENT_SECRET:client_secret,
            REFRESH_TOKEN:getRefreshToken(),
            GRANT_TYPE:REFRESH_TOKEN
        }

        from datetime import datetime,timedelta
        now = datetime.now()

        response=makeRequest("POST",url,params=params)
        decodedResponseData = json.loads(response.decode(ENCODING))

        if ERROR_CODE and ERROR not in decodedResponseData:

            data = lastGeneratedOauth if len(lastGeneratedOauth) > 0 else decodedResponseData
            EXPIRES_IN="expires_in" if "expires_in_sec" not in decodedResponseData else "expires_in_sec"     
            data[VALID_UNTIL]=now+timedelta(seconds=decodedResponseData[EXPIRES_IN])
            data[ACCESS_TOKEN]=decodedResponseData[ACCESS_TOKEN]    
            data[REFRESH_TOKEN]=params[REFRESH_TOKEN]
            
            writeToFile(os.path.join(PATH,CLIENT_FILE),data)

        else:
            print(decodedResponseData)
            print(message_REFRESH_TOKEN_ERROR)

    except Exception as e:
        print(decodedResponseData)
        print(e.__class__,e.args)


def getAccessToken():
#This method returns the access_token stored in the file, it will refresh if the token has expired and return the updated token. It returns only the access_token as a string. 

    data = readFromFile(os.path.join(PATH,CLIENT_FILE))
    
    from datetime import datetime,timedelta
    now = datetime.now()
    
    isFileEmpty= data is None
    
    isAccessTokenAvailable = not isFileEmpty and ACCESS_TOKEN in data

    isValidityAvailable = not isFileEmpty and VALID_UNTIL in data

    isValid = isValidityAvailable and now <= datetime.strptime(data[VALID_UNTIL],datetime_format)

    isAccessTokenValid = isAccessTokenAvailable and isValid

    isRefreshTokenAvailable = not isFileEmpty and REFRESH_TOKEN in data

    if isAccessTokenValid :
        return data[ACCESS_TOKEN]

    else :
        if isRefreshTokenAvailable:
            refreshAccessToken()
            data = readFromFile(os.path.join(PATH,CLIENT_FILE))
        else :
            generateAccessToken()
            data = readFromFile(os.path.join(PATH,CLIENT_FILE))
            
    return data[ACCESS_TOKEN] if data is not None and ACCESS_TOKEN in data else None

def getRefreshToken():
#This method returns refresh_token stored in the file (if available).

    data = readFromFile(os.path.join(PATH,CLIENT_FILE))
    return data[REFRESH_TOKEN] if data is not None else None

def getAccessTokenValidity():
#This method returns validity of the access_token stored in the file (if available).

    data = readFromFile(os.path.join(PATH,CLIENT_FILE))
    return data[VALID_UNTIL] if data is not None else None

def getAccessTokenWithHeader():
#This method returns the access token inside the accepted header format .
# {
# "Accept":"application/json; version=2.1" ,
# "Authorization":"Zoho-oauthtoken xyz1234..."
# }
#

    try:
        accessToken = getAccessToken()
        if accessToken is None:
            return None
    except:
        print()
   
    header[AUTHORIZATION]=TOKEN_PREFIX+getAccessToken()
    return header      
       
#===================================================================================================#

# Function to get monitor details by name
def get_monitor_details_by_name(monitor_name):
    access_token = getAccessToken()  # Use the existing function to get the access token
    url = f"https://www.site24x7.com/api/monitors/name/{monitor_name}"
    headers = {
        "Accept": "application/json; version=2.1",
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        monitor_details = response.json()
        return monitor_details
    else:
        print(f"Failed to fetch monitor details. Status code: {response.status_code}")
        return None

# Function to delete a monitor
def delete_monitor(monitor_id, hostname):
    access_token = getAccessToken()  # Use the existing function to get the access token
    url = f"https://www.site24x7.com/api/monitors/{monitor_id}"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json;charset=UTF-8"
    }

    response = requests.delete(url, headers=headers)

    response_data = response.json()
    status = response_data.get("message")

    if status == "success":
        print(f"Your hostname '{hostname}' with ID '{monitor_id}' has been successfully deleted.")
    else:
        print(f"Failed to delete monitor {monitor_id}. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Main script
monitor_name = input("Enter the monitor name: ")
monitor_details = get_monitor_details_by_name(monitor_name)
if monitor_details:
    monitor_id = monitor_details.get("data", {}).get("monitor_id")
    if monitor_id:
        print(f"Deleting your Monitor ID: {monitor_id}" + " from Site24x7 records.")
        delete_monitor(monitor_id, monitor_name)
    else:
        print("Monitor ID not found in the response.")
else:
    None

#================================================================
#Flask Server code to act as trigger.
# app = Flask(__name__)

# # Your existing functions (e.g., getAccessToken, get_monitor_details_by_name, delete_monitor, etc.)

# @app.route('/delete_monitor', methods=['POST'])
# def delete_monitor_endpoint():
#     data = request.json
#     monitor_name = data.get('monitor_name')
    
#     if not monitor_name:
#         return jsonify({'status': 'failed', 'message': 'Monitor name is required'}), 400
    
#     monitor_details = get_monitor_details_by_name(monitor_name)
#     if monitor_details:
#         monitor_id = monitor_details.get("data", {}).get("monitor_id")
#         if monitor_id:
#             delete_monitor(monitor_id, monitor_name)
#             return jsonify({'status': 'success', 'message': f'Monitor {monitor_name} deleted successfully'}), 200
#         else:
#             return jsonify({'status': 'failed', 'message': 'Monitor ID not found'}), 404
#     else:
#         return jsonify({'status': 'failed', 'message': 'Monitor details not found'}), 404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
