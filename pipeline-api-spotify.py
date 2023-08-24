import requests
import configparser
import base64
import json
import boto3

# READ SPOTIFY API DOCUMENTATION FOR BETTER UNDERSTANDING PRE-REQUISITES

# Client Credentials  --->  Acess Token
#        Acess Token  --->  API Requests



# Get access Client Credentials
parser = configparser.ConfigParser()
parser.read("pipeline.conf")

client_id = parser.get("spotify_api" , "client_id")
client_secret = parser.get("spotify_api" , "client_secret")



# As spotify requested, put Client Credentials string in base64
cc_string = client_id + ':' + client_secret  # build client_credentials string
string_bytes = cc_string.encode('ascii')  # string converted to type bytes based on 'ascii' table

bytes_base64 = base64.b64encode(string_bytes)  # string converted to type base64-bytes
string_base64 = bytes_base64.decode('ascii')  # string is still in encoded format but now back to type string, not bytes



# POST request --> obtain access token
url_post = "https://accounts.spotify.com/api/token"

header_post = {"Authorization": f"Basic {string_base64}", 
               "Content-Type": "application/x-www-form-urlencoded"}  # required headers parameters

payload = {"grant_type": 'client_credentials'}  # payload = required body parameter

response_post = requests.request("POST", url=url_post, headers=header_post, data=payload)  # retuns a dictionary in which one of the keys is 'access_token'

access_token = response_post.json()['access_token']



# GET request --> obtain desired data
url_get = "https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg"  # pitbull ID endpoint

header_get = {"Authorization": f"Bearer {access_token}"}  # required only header parameter

response_get = requests.request("GET", url=url_get, headers=header_get)

data = response_get.json()



# Write json file
local_filename = "pitbull_spotify_data.json"

with open(local_filename, "w") as fp:
    json.dump(data, fp)



# Send json to S3 Bucket
access_key = parser.get("aws_boto_credentials", "access_key")
secret_key = parser.get("aws_boto_credentials", "secret_key")
bucket_name = parser.get("aws_boto_credentials", "bucket_name")

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

s3_file = local_filename
s3.upload_file(local_filename, bucket_name, s3_file)