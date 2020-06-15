import os
from pytrics.tools import Tools
from pytrics_rework.pytrics_rework.operations.download import get_survey_json
from pytrics.common.constants import (
    ENV_VAR_ABSOLUTE_PATH_TO_DATA_DIR,
)

def pytrics_get():

    tools = Tools()

    try:
        tools.retrieve_survey_response_data('SV_eQl4Bl9zA0b9rHD')
    except EnvironmentError as e:
        print("EnvironmentError")
        print("Error Encountered")
        return("Problem with accessing data")
    except Exception as e:
        print("Unknown error")
        print(e)
    finally:
        return("Complete")

def pytrics_data():
    response_file_json = None
    abs_path_to_data_dir = os.environ.get(ENV_VAR_ABSOLUTE_PATH_TO_DATA_DIR, '')
    
    try:
        response_file_json = get_survey_json('SV_eQl4Bl9zA0b9rHD', abs_path_to_data_dir)
    except Exception as e:
        print("Unknown Exception")
        print(e)
    finally:
        return response_file_json