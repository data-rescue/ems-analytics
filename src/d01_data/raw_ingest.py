from pathlib import Path, PureWindowsPath
from configparser import ConfigParser
import boto3
import json
import datetime

# https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
# https://docs.python.org/3/library/configparser.html


config_file = Path.cwd().parents[2].joinpath('configs', 'conf_local.ini')

config = ConfigParser()
config.read(config_file)

ACCESS_KEY = config['AWS_SESSION']['ACCESS_KEY_ID']
SECRET_KEY = config['AWS_SESSION']['SECRET_ACCESS_KEY']
REGION_NAME = config['AWS_SESSION']['REGION_NAME']
BUCKET_NAME = config['s3']['PRI_BUCKET_NAME']
#print(ACCESS_KEY)

#s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

aws_session = boto3.Session(aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY, 
                            region_name=REGION_NAME)

s3client = aws_session.client('s3')
response = s3client.list_objects(Bucket=BUCKET_NAME)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
print(json.dumps(response, indent=4, default=myconverter))
#client.list_buckets()

def upload_file(folder, file, s3):
    file_path = Path.cwd().parents[0].joinpath(folder, file)
    remote_path = Path.joinpath(folder, file)

    try:
        s3.Bucket(BUCKET_NAME).upload_file(file_path, remote_path)
    except:
        print('upload error')


def download_file(folder, file, s3):
    file_path = Path.cwd().parents[0].joinpath(folder, file)

    try:
        s3.Bucket(BUCKET_NAME).download_file(file_path, file_path)

    except:
        print('download error')


def list_bucket_content(s3):
    json.dumps(response, indent=4, default=myconverter)
    


#list_bucket_content(s3)


"""
    config = ConfigParser()
    config.read(config_file)

    __ACCESS_KEY = config['AWS_SESSION']['ACCESS_KEY_ID']
    __SECRET_KEY = config['AWS_SESSION']['SECRET_ACCESS_KEY']
    __REGION_NAME = config['AWS_SESSION']['REGION_NAME']
    __BUCKET_NAME = config['s3']['PRI_BUCKET_NAME']
"""


"""
    aws_session = boto3.Session(aws_access_key_id=ACCESS_KEY,
                                aws_secret_access_key=SECRET_KEY,
                                region_name=REGION_NAME)
    
    def __init__(self, folder, file):
        self._folder = folder
        self._file = file

    def remote_object_list():
        print(json.dumps(response, indent=4, default=myconverter))

    def _myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
"""


def __init__(self, folder, file):
        self.folder = folder
        self.file = file


def get_config_file_path():
        config_file = Path.cwd().parents[2].joinpath(
            'configs', 'conf_local.ini')

    return config_file
