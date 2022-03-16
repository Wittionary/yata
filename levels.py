import json
import requests as r
from todoist_api_python.api import TodoistAPI
from datetime import datetime

with open("config.json", "r") as f:
    config = json.load(f)
    api = TodoistAPI(config['todoist']['api_key'])
    api_key = config['todoist']['api_key']

endpoint_url = "https://api.todoist.com/sync/v8"
headers = {"Authorization": f"Bearer {api_key}"}

def auth_sync_api():
    """
    Authenticate to the Todoist Sync API
    """

def initial_sync():
    """
    The first sync you run when there's no data at all
    """
    path = "/sync"
    payload = {"sync_token":"*", "resource_types":'["projects"]'}
    response = r.post(f"{endpoint_url}{path}", headers=headers, data=payload)
    response = json.loads(response.content)
    with open("todoist-storage.json", "w") as f:
        f.write(str(response))

    sync_token = response["sync_token"]
    return sync_token

def get_completed_tasks(since="2007-4-29T10:13"):
    """
    Get all completed tasks
    """
    path = "/completed/get_all"
    payload = {"since":f"{since}"}
    response = r.post(f"{endpoint_url}{path}", headers=headers, data=payload)
    response = json.loads(response.content)

    with open("todoist-storage.json", "w") as f:
        f.write(str(response))

    last_sync = get_now()
    set_levels_storage("last_sync", last_sync)
    return

def get_now():
    """
    Returns a Todoist-formatted datetime string
    e.g. 2022-03-11T05:35
    TODO: Test if it needs UTC or client timezone
    """
    now = datetime.utcnow().isoformat()
    now_list = now.split(":")
    now = f"{now_list[0]}:{now_list[1]}"
    return now

def set_levels_storage(key, value):
    # open file
    with open("levels-storage.json", "r") as f:
        levels_storage = json.load(f)

    # Add key-value pair to storage object
    levels_storage[key] = value

    with open("levels-storage.json", "w") as f:
        f.write(str(levels_storage))

    return

def get_levels_storage(key):
    """
    Return the value of an object in app storage
    """
    with open("levels-storage.json", "r") as f:
        levels_storage = json.load(f)

    value = levels_storage[key]    
    
    return value


# App logic -------------------------------------------------

#sync_token = initial_sync()
get_completed_tasks()
# Store the last_sync so we can check to see how far back we shoud look for newly/recently completed tasks
# That probably belongs at the end of the get_completed_tasks() func

# MVP
# - checks to see when item(s) have been completed
# - add points to experience system
# - reflect XP increase in frontend

# Test stuff with a sample project