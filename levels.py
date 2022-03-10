import json
import requests as r
from todoist_api_python.api import TodoistAPI

with open("config.json", "r") as f:
    config = json.load(f)
    api = TodoistAPI(config['todoist']['api_key'])
    api_key = config['todoist']['api_key']

endpoint_url = "https://api.todoist.com/sync/v8/sync"
headers = {"Authorization": f"Bearer {api_key}"}

def auth_sync_api():
    """
    Authenticate to the Todoist Sync API
    """

def initial_sync():
    """
    The first sync you run when there's no data at all
    """
    payload = {"sync_token":"*", "resource_types":'["projects"]'}
    response = r.post(endpoint_url, headers=headers, data=payload)
    response = json.loads(response.content)
    with open("storage.json", "w") as f:
        f.write(str(response))

    sync_token = response["sync_token"]
    return sync_token


# App logic -------------------------------------------------

sync_token = initial_sync()

# So now I need to add something that
# - checks to see when item(s) have been completed
# - add points to experience system
# - reflect XP increase in frontend

# Test stuff with a sample project