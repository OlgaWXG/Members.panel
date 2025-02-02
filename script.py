import requests
import clr
from RevitServices.Persistence import DocumentManager

# Constants for API access
CLIENT_ID = "WLlYmqfTa0zBfHm8EFJyjXYhJECn9K7MCn9yGtSAsfzooJLT"  # Replace with your actual Client ID
CLIENT_SECRET = "1cl7nGpSkOecFZKTMFWykod1xlUmWdXlAPJTz6ZrvHzFsJHB4qOYGhAOphmfbsha1cl7nGpSkOecFZKTMFWykod1xlUmWdXlAPJTz6ZrvHzFsJHB4qOYGhAOphmfbsha"  # Replace with your actual Client Secret
TOKEN_URL = "https://developer.api.autodesk.com/authentication/v1/authenticate"
HUBS_URL = "https://developer.api.autodesk.com/project/v1/hubs"
PROJECTS_URL = "https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"

# Global variable for the access token
access_token = None

def get_access_token():
    """ Retrieves a new access token """
    global access_token

    if access_token is None:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "data:read"
        }

        response = requests.post(TOKEN_URL, data=data)
        if response.status_code == 200:
            access_token = response.json()["access_token"]
        else:
            print("Error obtaining token:", response.text)

    return access_token

def get_hubs():
    """ Retrieves the list of hubs """
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(HUBS_URL, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print("Error obtaining hubs:", response.text)
        return []

def get_projects(hub_id):
    """ Retrieves projects for the specified hub """
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    url = PROJECTS_URL.format(hub_id=hub_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print("Error obtaining projects:", response.text)
        return []

# Testing
if __name__ == "__main__":
    hubs = get_hubs()
    if hubs:
        for hub in hubs:
            print("Hub Name:", hub["attributes"]["name"])
            hub_id = hub["id"]
            projects = get_projects(hub_id)
            for project in projects:
                print("Project Name:", project["attributes"]["name"])
                print("Project ID:", project["id"])
