from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Root endpoint to confirm app is running
@app.get("/")
async def root():
    return {"message": "App is running"}

# Define the request model
class NotionContent(BaseModel):
    content: str

# Endpoint to add text to Notion
@app.post("/add_to_notion")
async def add_to_notion(content: NotionContent):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_API_TOKEN')}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"page_id": os.getenv("NOTION_PAGE_ID")},
        "properties": {
            "title": {
                "title": [{"text": {"content": content.content}}]
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return {"status": response.status_code, "data": response.json()}

# Endpoint to retrieve text from Notion (simplified for example)
@app.get("/retrieve_from_notion")
async def retrieve_from_notion():
    url = f"https://api.notion.com/v1/pages/{os.getenv('NOTION_PAGE_ID')}"
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_API_TOKEN')}",
        "Notion-Version": "2022-06-28"
    }
    response = requests.get(url, headers=headers)
    return {"status": response.status_code, "data": response.json()}
