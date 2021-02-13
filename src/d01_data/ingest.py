from pathlib import Path, PureWindowsPath
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

__project_root = proj_utils.get_project_file_path()
__config_file = PureWindowsPath(
    Path(__project_root).joinpath('configs', 'conf_local.ini'))

## CREATE CONFIGURATION OBJECT
## 
## The next two lines of code instantiates a configuration object
## and reads the content of the configuration file.
__config = ConfigParser()
__config.read(__config_file)

## DEFINE SESSION ATTRIBUTES AND BUCKET NAME
__ACCESS_KEY = __config['AWS_SESSION']['ACCESS_KEY_ID']
__SECRET_KEY = __config['AWS_SESSION']['SECRET_ACCESS_KEY']
__REGION_NAME = __config['AWS_SESSION']['REGION_NAME']
_BUCKET_NAME = __config['s3']['PRI_BUCKET_NAME']

## CREATE SESSION OBJECT
try:
    _aws_session = boto3.Session(aws_access_key_id=__ACCESS_KEY,
                                 aws_secret_access_key=__SECRET_KEY,
                                 region_name=__REGION_NAME)

except botocore.exceptions.ParamValidationError as error:
    raise ValueError('The parameters you provided are incorredct: {}'.format(error))


class ProjectIngest:
        
    def __init__(self, folder, file):
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
        self.__valid_folders = ['01_raw', '02_intermediate',
                                '03_processed', '04_models', '05_model_input', '06_reporting']

        if type(folder) is not str: # Validate input 'folder' as string type
            raise TypeError("Please enter a string value for the folder attribute.")
        
        if folder not in self.__valid_folders: # Validate folder exist
            raise TypeError("Please check your folder selection. Valid options are "\
                            "01_raw, 02_intermediate, 03_processed, 04_models, "\
                            "05_model_input, and 06_reporting")
        
        if type(file) is not str: # Validate input 'file' as string type
            raise TypeError("Please enter a string value for the file attribute")

        self.__folder = folder
        self.__file = file
        
        
        
        

    def remote_object_list(self):
        """
        The method intends to provide a list of the files/objects that
        are stored in AWS S3. This will allow the team look at the files
        that has been stored.

        This method will use the Class attribute folder to provide the list
        of objects stored in the specific s3 folder.        
        """
        try:
            __s3client=_aws_session.client('s3')       
            __response = __s3client.list_objects(Bucket=_BUCKET_NAME, Prefix=self.__folder)
        except:
            print("S3 client creation error for ")
        __object_list = list()

        for item in __response['Contents']:
            if item['Key'] != str(self.__folder + "/"):
                __object_list.append(item['Key'])

        return(__object_list)
       


#ingest = ProjectIngest('01_raw', '20210213-ems-raw.xlsx')

ingest = ProjectIngest('01_raw', '20210213-ems-raw.xlsx')

ingest.remote_object_list()
