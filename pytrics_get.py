from pytrics.tools import Tools

def pytrics_get():

    tools = Tools()

    try:
        tools.retrieve_survey_response_data('SV_eQl4Bl9zA0b9rHD')
    except EnvironmentError:
        print("EnvironmentError")
        print("Error Encountered")
        return("Problem with accessing data")
    except Exception as e:
        print("Unknown error")
        print(e)
    finally:
        return("Complete")