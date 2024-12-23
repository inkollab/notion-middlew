from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx

# Initialize the FastAPI application
app = FastAPI()

# Root endpoint to confirm the app is running
@app.get("/")
async def root():
    return {"message": "App is running"}

# Define the request model for task creation
class Task(BaseModel):
    description: str
    phase: str = "Brainstorm"  # Default phase
    status: str = "Pending"    # Default status

# New endpoint to create a task in the Notion database
@app.post("/create_task")
async def create_task(task: Task):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_API_TOKEN')}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": os.getenv("NOTION_DATABASE_ID")},  # Use the Database ID
        "properties": {
            "Name": {
                "title": [{"text": {"content": task.description}}]
            },
            "Phase": {
                "select": {"name": task.phase}
            },
            "Status": {
                "select": {"name": task.status}
            }
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"status": response.status_code, "data": response.json()}

# Endpoint to add general content to Notion (for other types of pages)
class NotionContent(BaseModel):
    content: str

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
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"status": response.status_code, "data": response.json()}

# Endpoint to retrieve a page from Notion (simplified for example)
@app.get("/retrieve_from_notion")
async def retrieve_from_notion():
    url = f"https://api.notion.com/v1/pages/{os.getenv('NOTION_PAGE_ID')}"
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_API_TOKEN')}",
        "Notion-Version": "2022-06-28"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return {"status": response.status_code, "data": response.json()}
