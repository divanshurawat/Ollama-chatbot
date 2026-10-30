
from datetime import datetime
import json
import requests

from Utilities.utilities import log


def get_current_time():
    return datetime.now().strftime("%y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=4"
    response= requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def get_user_city():
    return "Mumbai"




TOOLS=[
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"Get the current time in the format of dd-mm-yy HH:MM:SS",
            "parameters":{
                "type":"object",
                "properties":{ }
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_current_weather",
            "description":"Get the current weather of a given city. If the user did not name a city (e.g. 'my city'), call get_user_city first to find it - never ask the user for their city.",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":  "string",
                        "description": "City to get the weather for.",
                    }
                },
                "required":["city"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_user_city",
            "description":"Returns the name of the city where the user currently is. Takes NO arguments - you do not need to know anything to call it. Call this whenever the user says 'my city', 'my location', 'here', 'where am I', or asks something about their location without naming a city. Example: for 'weather of my city', call get_user_city first, then call get_current_weather with the returned city.",
            "parameters":{
                "type":"object",
                "properties":{ },
            }
        }
    }
    
]

FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time":get_current_time,
    "get_current_weather": get_city_weather,
    "get_user_city": get_user_city
}

def run_tool(tool_call):
    fuc_name= tool_call.function.name
    fuc_args={}

    try:
        fuc_args= json.loads(tool_call.function.arguments or "{}")
        fn= FUNCTION_NAME_TO_FUNCTION_MAP.get(fuc_name)
        log(f">> {fuc_name}({fuc_args})")
        result= fn(**fuc_args)
        
    except Exception as e:
        result= f"Error calling {fuc_name} with args {fuc_args}: {e}"

    log(f"  >{result}")
    return result