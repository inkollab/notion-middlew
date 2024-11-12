import requests
import os

# Set your Notion API token and parent page ID
NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN') or "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"
PARENT_PAGE_ID = os.getenv('PARENT_PAGE_ID') or "13565aafd05e807b8287c165db2366a6"

# Define headers for the Notion API
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Define the payload for creating a database with properties
data = {
    "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
    "title": [
        {
            "type": "text",
            "text": {"content": "Task Management Database"}
        }
    ],
    "properties": {
        "Name": {"title": {}},
        "Phase": {
            "select": {
                "options": [
                    {"name": "Brainstorm", "color": "blue"},
                    {"name": "Blueprint", "color": "purple"},
                    {"name": "Development", "color": "green"},
                    {"name": "Review", "color": "yellow"}
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "Pending", "color": "gray"},
                    {"name": "In Progress", "color": "orange"},
                    {"name": "Completed", "color": "green"}
                ]
            }
        }
    }
}

# Make the API request to create the database
response = requests.post(
    "https://api.notion.com/v1/databases",
    headers=headers,
    json=data
)

# Check the response and output the result
if response.status_code == 200:
    print("Database created successfully!")
    print("Database ID:", response.json().get("id"))
else:
    print("Failed to create database:", response.json())
