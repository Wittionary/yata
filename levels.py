# MVP
# - checks to see that item(s) have been completed
# - add points to experience system
# - reflect XP increase in frontend

#from genericpath import exists
import json, time
from telnetlib import theNULL
import requests as r
from todoist_api_python.api import TodoistAPI
from datetime import datetime
from os import path

TODOIST_STORAGE_FILENAME = "todoist-storage.json"
APP_STORAGE_FILENAME = "levels-storage.json"

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
    with open(TODOIST_STORAGE_FILENAME, "w") as f:
        f.write(str(response))

    sync_token = response["sync_token"]
    return sync_token

def get_completed_tasks(since="2007-4-29T10:13"):
    """
    Get all completed tasks
    """
    print("Pulling completed tasks from Todoist API")
    path = "/completed/get_all"
    payload = {"since":f"{since}"}
    response = r.post(f"{endpoint_url}{path}", headers=headers, data=payload)
    response = json.loads(response.content)

    with open(TODOIST_STORAGE_FILENAME, "w") as f:
        f.write(str(json.dumps(response)))

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
    # Create the storage file if it's not there
    file_exists = path.exists(APP_STORAGE_FILENAME)
    if not file_exists:
        with open(APP_STORAGE_FILENAME, "w") as f:
            print(f"Creating {APP_STORAGE_FILENAME}")
        levels_storage = {}
    else:
        # open file
        with open(APP_STORAGE_FILENAME, "r") as f:
            levels_storage = json.load(f)

    # Add key-value pair to storage object
    levels_storage[key] = value

    with open(APP_STORAGE_FILENAME, "w") as f:
        f.write(str(json.dumps(levels_storage)))

    return

def get_levels_storage(key):
    """
    Return the value of an object in app storage
    """
    with open(APP_STORAGE_FILENAME, "r") as f:
        levels_storage = json.load(f)

    value = levels_storage[key]    
    
    return value

def get_todoist_storage(key):
    """
    Return the value of an object in app storage
    """
    with open(TODOIST_STORAGE_FILENAME, "r") as f:
        todoist_storage = json.load(f)

    value = todoist_storage[key]
    #print(f"{value}")    
    
    return value

def completed_tasks_count():
    count = len(get_todoist_storage("items"))
    return count

def increment_experience_points():
    # add some numbers to levels storage
    return

# App logic -------------------------------------------------

#sync_token = initial_sync()
# DONE: Store the last_sync so we can check to see how far back we should look for newly/recently completed tasks
# DONE: That probably belongs at the end of the get_completed_tasks() func

get_completed_tasks()

#time.sleep(10)
num_completed = completed_tasks_count()
print(f"Num completed is: {num_completed}")
print("Sleeping 20 seconds")
time.sleep(20)
get_completed_tasks(get_levels_storage("last_sync"))
new_num_completed = completed_tasks_count()
print(f"New num completed is: {new_num_completed}")

if new_num_completed > num_completed:
    increment_experience_points()
