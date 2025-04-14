from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from ai import document_handler_agent
from database.config import get_db_connection
from prisma import Client
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentInput(BaseModel):
    doc: str

@app.post("/documents/")
async def process_document(input: DocumentInput, db: Client = Depends(get_db_connection)):
    doc = input.doc
    print("Processing document:", doc)
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
    return result

@app.get("/documents/")
async def get_documents(db: Client = Depends(get_db_connection)):
    try:
        documents = await db.document.find_many()
        return documents
    except Exception as e:
        print(f"Error fetching documents: {e}")
        return {
            "status": "error",
            "message": "Failed to fetch documents from the database.",
            "error_details" : str(e)
        }