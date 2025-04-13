from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from ai import document_handler_agent
from database.config import get_db_connection
from prisma import Client


app = FastAPI()

# app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/documents/")
async def process_document(doc: str, db: Client = Depends(get_db_connection)):
    initial_state = {
        "document": doc,
        "messages": []
    }
    result = document_handler_agent.agent.invoke(initial_state)
    print("Result:", result)

    await db.document.create(data={
        "title": result["title"],
        "summary": result["summary"],
        "tags": result["tags"],
        "category": result["category"],
        "document": doc,
    })
    # Save to PG and ChromaDB
    return result

