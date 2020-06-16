import os
from zipfile import ZipFile
from requests import HTTPError
import json
import io
import time

from pytrics.tools import Tools
from pytrics.common.constants import (
    ENV_VAR_ABSOLUTE_PATH_TO_DATA_DIR,
    QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT
)
from pytrics.qualtrics_api.common import get_details_for_client
from pytrics.qualtrics_api.client import QualtricsAPIClient
from pytrics.common.exceptions import (
    QualtricsAPIException,
    QualtricsDataSerialisationException,
)
from pytrics.common.constants import (
    QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT,
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
    
    base_url, auth_token = get_details_for_client()
    api = QualtricsAPIClient(base_url, auth_token)

    try:
        response_file_json = save_responses_to_file(api, 'SV_eQl4Bl9zA0b9rHD', abs_path_to_data_dir)
    except QualtricsDataSerialisationException as qex:
        raise qex

    """ try:
        response_file_json = get_survey_json('SV_eQl4Bl9zA0b9rHD', abs_path_to_data_dir)
    except Exception as e:
        print("Unknown Exception")
        print(e)
    finally:
        return response_file_json """
    
    return response_file_json

def save_responses_to_file(api, survey_id, abs_path_to_data_dir, progress_id=None, retries=0):
    # file_path_and_name = _get_response_file_path(survey_id, abs_path_to_data_dir)
    response_bytes = None
    json_data = None
    
    if retries == 0:
        _, progress_id = api.create_response_export(survey_id)

    try:
        response_bytes = _await_response_file_creation(api, survey_id, progress_id)
    except (QualtricsDataSerialisationException, HTTPError, KeyError):
        if retries < QUALTRICS_API_EXPORT_RESPONSES_RETRY_LIMIT:
            retries += 1
            # Recurse to get new progress_id and try again
            save_responses_to_file(api, survey_id, abs_path_to_data_dir, progress_id, retries)
        else:
            # Retry limit reached
            raise QualtricsDataSerialisationException('Failed after {0} attempts to get responses for survey_id {1}'.format(
                retries,
                survey_id,
            ))

    # CREATE AN INTERNAL OBJECT AS ZIP FILE

    # print(type(response_bytes))
    zf = ZipFile(io.BytesIO(response_bytes), "r")
    # print("zf created")
    for item in zf.filelist:
        # print(item)
        with zf.open(item) as json_file:
            json_data = json.load(json_file)
            # print(data)

    """ if response_bytes:
        try:
            print(file_path_and_name)
            with open(file_path_and_name, mode='wb') as response_file:
                response_file.write(response_bytes)

        except Exception as ex:
            raise QualtricsDataSerialisationException(ex) """

    return json_data

def _await_response_file_creation(api, survey_id, progress_id):
    status = 'inProgress'
    file_id = None

    while status not in ['complete', 'failed']:
        time.sleep(QUALTRICS_API_EXPORT_RESPONSES_PROGRESS_TIMEOUT)

        data, file_id = api.get_response_export_progress(survey_id, progress_id)

        status = data['result']['status']

    if status == 'failed' or not file_id:
        raise QualtricsDataSerialisationException('Failed to complete export for progress_id {}'.format(progress_id))

    return api.get_response_export_file(survey_id, file_id)