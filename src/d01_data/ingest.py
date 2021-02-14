from pathlib import Path, PureWindowsPath
import os
from configparser import ConfigParser
import json
import datetime
import boto3  # AWS library
import botocore # AWS library

from src.d00_utils import proj_utils

## ENCAPSULATION CONCEPT:
##
## I have attempted to implement the concept of encapsulation 
## in this class to avoid having every variable available when 
## using the ProjectIngest class in Jupyter Labs or Jupyter 
## Notebooks. 
##
## The variables or methods with double underscore are private and 
## they are not needed in any of the methods or sub classes
##
## The variables or methods with one underscore are protected and
## they are not needed in any of the methods or sub classes 
##
## Variables and methods without any underscore are the particular
## functionalities that are most useful in Jupyter Notebooks and
## Jupyter Labs


## DEFINE CONFIGURATION FILE PATH
##
## The next two steps are created to define the the path where
## the configuration file will be stored with the necessary
## credential informations to access AWS S3 bucket.
##
## Useful Documentation:
##      https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
##      https://docs.python.org/3/library/configparser.html

_project_root = proj_utils.get_project_file_path()
__config_file = PureWindowsPath(
    Path(_project_root).joinpath('configs', 'conf_local.ini'))

## CREATE CONFIGURATION OBJECT
## 
## The next two lines of code instantiates a configuration object
## and reads the content of the configuration file.
__config = ConfigParser()
__config.read(__config_file)

## DEFINE SESSION ATTRIBUTES AND BUCKET NAME
try:
    __ACCESS_KEY = __config['AWS_SESSION']['ACCESS_KEY_ID']
    __SECRET_KEY = __config['AWS_SESSION']['SECRET_ACCESS_KEY']
    __REGION_NAME = __config['AWS_SESSION']['REGION_NAME']
    _BUCKET_NAME = __config['s3']['PRI_BUCKET_NAME']
except:
    raise TypeError('CONFIG FILE PARAMETERS ERROR: Review config file and variable call outs.')

## CREATE SESSION OBJECT
_aws_session = boto3.Session(aws_access_key_id=__ACCESS_KEY,
                             aws_secret_access_key=__SECRET_KEY,
                             region_name=__REGION_NAME)

_valid_folders = ['01_raw', '02_intermediate',
                  '03_processed', '04_models', '05_model_input', '06_reporting']
class ProjectIngest:
        
    def __init__(self, sub_folder, file):
        """
        A class created to upload, download, and list objects from a remote s3 bucket into
        your project local data folders.
        
        Parameters
        ----------
            folder : string (mandatory)
                The string will represent one of the 6 data folders defined in the project
                structure (i.e., 01_raw, 02_intermediate, 03_processed, 04_models,
                05_model_input, 06_reporting)

            file : string (mandatory)
                The string will represent the name of the file you are trying to upload or
                download. The file naming convention to be followed is DATE (YYYYMMDD) + 
                INITIALS + SHORT DELIMITED DESCRIPTION.

                An example could be: 20210213-ans-gender-medication-model.csv

                The naming convention will not be enforced but should be followed to
                help finding individual models or datasets.
        
        Methods
        -------
            remote_object_list()
        """
        

        # Validation of input parameters for class generation
        if type(sub_folder) is not str: # Validate input 'folder' as string type
            raise TypeError("Class Creation: Please enter a string value for the folder attribute.")
        
        if sub_folder not in _valid_folders: # Validate folder exist
            raise TypeError("Class Creation: Please check your folder selection. Valid options are "\
                            "01_raw, 02_intermediate, 03_processed, 04_models, "\
                            "05_model_input, and 06_reporting")
        
        if type(file) is not str: # Validate input 'file' as string type
            raise TypeError("Class Creation: Please enter a string value for the file attribute")
        
        # Assignment of validated input parameters to the instance object
        self.__sub_folder = sub_folder
        self.__file = file

        # Internal Class Variables
        self.__project_name = 'ems-analytics'

        self.__ingest_folder = 'data'

        self.__local_file_path = PureWindowsPath(
            Path(_project_root).joinpath(self.__project_name,
                                         self.__ingest_folder,
                                         self.__sub_folder,
                                         self.__file))

        self.__s3_key = (self.__sub_folder + "/" + self.__file)
        
        
    def remote_object_list(self):
        """
        The method intends to provide a list of the files/objects that
        are stored in AWS S3. This will allow the team look at the files
        that has been stored.

        This method will use the Class attribute folder to provide the list
        of objects stored in the specific s3 folder.        
        """
        
        try:
            __response = _aws_session.client('s3').list_objects(
                Bucket=_BUCKET_NAME, Prefix=self.__sub_folder)

        except botocore.exceptions.ParamValidationError as error:
            raise ValueError(
                'The parameters you provided are incorredct: {}'.format(error))

        __object_list = list()

        for item in __response['Contents']:
            if item['Key'] != str(self.__sub_folder + "/"):
                __object_list.append(item['Key'])

        return(__object_list)

    def local_download(self):
        """
        Note 1: Need to document
        Note 2: After initial assessment of the raw data, we could refactor to include an efficient indexing
        Note 3: Instead of generic download, I will refactor to intentional downloads (e.g., local_download_ems_raw())
        """
        
        if not os.path.exists(self.__local_file_path):
            try:
                __response = _aws_session.client('s3').download_file(
                    Bucket=_BUCKET_NAME, 
                    Key=str(self.__s3_key),
                    Filename=str(self.__local_file_path))
            
            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code'] == "404":
                    print("The {} file does not exist in the {} folder at the S3 bucket.".format(self.__file, self.__sub_folder))
                else:
                    raise
        else:
            print('{} file already exist in your local {} folder'.format(self.__file, self.__sub_folder))

"""
#### CODE IS STILL WORK IN PROGRESS
    def __s3_key_exist(self):
        s3 = boto3.resource('s3')

        try:
            s3.Object(Bucket=_BUCKET_NAME,
                      Key=str(self.__s3_key)).load()

    def remote_upload(self):
        pass

    ###### ANOTHER POSIBLE APPROCH UPLOAD
    def upload_file(folder, file, s3):
        file_path = Path.cwd().parents[0].joinpath(folder, file)
    remote_path = Path.joinpath(folder, file)

    try:
        s3.Bucket(BUCKET_NAME).upload_file(file_path, remote_path)
    except:
        print('upload error')
"""

#ingest = ProjectIngest('01_raw', '20210213-ems-raw.xlsx')

#ingest = ProjectIngest('01_raw', '20210213-ems-raw.xlsx')

#ingest.remote_object_list()

ingest = ProjectIngest('01_raw', '20210213-admin-01-raw-test1.txt')

ingest.local_download()
