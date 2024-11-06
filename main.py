from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NotionContent(BaseModel):
    content: str

@app.post("/add_to_notion")
async def add_to_notion(content: NotionContent):
    # Placeholder for code to add to Notion
    return {"message": "Content added to Notion"}
