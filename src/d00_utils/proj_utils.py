from pathlib import Path, PureWindowsPath
import datetime

def get_project_file_path():
    """
    The utility function is intented to help us find the "projet root folder". The project
    root foolder is just the folder where we clone the git hub repo.

    This utility function is expected to help find the appropriate path quicker for our analytics.
    """
       
    for parent in Path.cwd().parents:
        if str(parent).find('ems-analytics') == -1:
            return parent

def datetime_converter_for_json_dumps(obj):
    """
    Many of the AWS responses will have a datetime object included and the function json.dumps()
    does not handle this type of objects. The solution to this problem was provided by Gabor Szabo
    in the blog titled 'How to serialize a datetime object as JSON using Python?'

    Blog: https://code-maven.com/serialize-datetime-object-as-json-in-python.
    Author: Gabor Szabo
    Title: How to serialize a datetime object as JSON using Python
    Publish Date: 2016-08-22
    """

    if isinstance(obj, datetime.datetime):
        return obj.__str__()   
