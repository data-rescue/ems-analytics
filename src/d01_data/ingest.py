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

_valid_file_extension = ['.csv', '.xlsx', '.html', '.parquet']
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
            raise TypeError("Instance Creation: Please enter a string value for the folder attribute.")
        
        if sub_folder not in _valid_folders: # Validate folder exist
            raise TypeError("Instance Creation: Please check your folder selection. Valid options are "\
                            "01_raw, 02_intermediate, 03_processed, 04_models, "\
                            "05_model_input, and 06_reporting")
        
        if type(file) is not str: # Validate input 'file' as string type
            raise TypeError("Instance Creation: Please enter a string value for the file attribute")

        if Path(file).suffix not in _valid_file_extension:
            raise TypeError("Instance Creation: Please validate that '{}' have a valid file extension".format(file))
        
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

    def local_download_gen(self):
        """
        The local_download_gen() method provides a flexible download experience, this method 
        will take the ProjectIngest class attributes <folder> and <file> to ingest an s3 object 
        to the appropriate project folder. S3 logical folder and project folder structure are
        designed to be equals.

        Properties:
        -----------
            No additional properties required
        
        Return
        ------
            S3 object / data file (e.g., raw.csv)
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

    def s3_key_exist(self):
        """
        The s3_key_exist() method is used to validate if an specific s3 key already exist in the s3
        bucket. An s3 key is just the logical path/folder structure used in the s3 bucket. For example,
        01_raw\20210213-admin-01-raw-test.txt is a fully defined key.

        Properties:
        -----------
            No additional properties required

        Return
        ------
            Boolean : Returns True or False depending whether the key exist or not.
        """
        
        try:
            _aws_session.resource('s3').Object(bucket_name=_BUCKET_NAME,
                                               key=str(self.__s3_key)).load()

        except botocore.exceptions.ClientError as error:

            if error.response['Error']['Code'] == "404":
                # The object does not exist
                return False
                
            else:
                # Something else has gone wrong.
                raise
        else:                        
            # The object does exist
            return True

    def remote_upload(self):
        """
        The remote_upload() method will upload your local project data file to the S3 bucket. Should
        be only used when the data model is ready for test and validation by another team member.

        Properties:
        -----------
            No additional properties required
        
        Return
        ------
            S3 object / data file (e.g., raw.csv)        
        """
        if self.s3_key_exist():
            # return message that a file with that name exist
            print('The {} file already exist in the S3 bucket under the key {}'.format(
                self.__file, self.__s3_key))
        else:
            # create the session and upload the file
            try:
                _aws_session.resource('s3').meta.client.upload_file(Filename=str(self.__local_file_path),
                                                                    Bucket=_BUCKET_NAME,
                                                                    Key=str(self.__s3_key))
            except botocore.exceptions.ClientError as error:
                raise

"""
    FUTURE WORK:
        Considering the idea of creating unique raw ingest files that takes the raw .xlsx file and:
        1. split each workshee of the work book in its separate csv modules
        2. validate each of the data modules created for proper dtype for each column
        3. Ingest the validated dtype columns and data module to the 01_raw folder 
"""
