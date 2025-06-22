from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from models import File, QueryReply, User
from vector_store import delete_file_from_qdrant
from agent import query_with_agent_and_return
from Cloudinary.upload_file import router as cloudinary_router
from Auth.routes import auth_router
from dependencies import get_current_user
from fastapi.middleware.cors import CORSMiddleware

origins=[
    "http://localhost:5173",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")
app.include_router(cloudinary_router)

# init_db()

# @app.post("/upload")
# def upload_file(file: UploadFile = Form(...), user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
#     file_id = str(uuid4())
#     file_url, file_key = upload_file_to_s3(file.file, file.filename, user.id)

#     temp_path = f"temp/{file_id}_{file.filename}"
#     with open(temp_path, "wb") as f:
#         f.write(file.file.read())

#     chunks = parse_file(temp_path)
#     vectors = embedding_model.embed_documents(chunks)
#     upsert_to_qdrant(vectors, chunks, user.id, file_id)

#     new_file = File(id=file_id, filename=file.filename, url=file_url, uploaded_at=datetime.now(timezone.utc), user_id=user.id)
#     db.add(new_file)
#     db.commit()

#     return {"message": "File uploaded", "file_id": file_id, "file_url": file_url}


@app.get("/query")
def query_file(file_id: str, question: str, user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
    file = db.query(File).filter_by(id=file_id, user_id=user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    response = query_with_agent_and_return(question, user.id, file_id)
    db.add(QueryReply(query=question, response=response, file_id=file_id))
    db.commit()

    return {"query": question, "response": response}


@app.get("/files")
def list_files(user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
    files = db.query(File).filter_by(user_id=user.id).all()
    return [{"file_id": f.id, "filename": f.filename, "url": f.url, "uploaded_at": f.uploaded_at} for f in files]


@app.delete("/file/{file_id}")
def delete_file(file_id: str, user: User = Depends(get_current_user), db: Session = Depends(SessionLocal)):
    file = db.query(File).filter_by(id=file_id, user_id=user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    delete_file_from_qdrant(user.id, file_id)
    db.delete(file)
    db.commit()
    return {"message": "File deleted"}

@app.get("/history")
def get_history(file_id:str, user:User = Depends(get_current_user),db:Session =Depends(SessionLocal)):
    result = (
    db.query(QueryReply)
    .filter(QueryReply.file_id == file_id)
    .order_by(QueryReply.created_at.asc())
    .all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No history found for this file")
    return [
        {
            "query": reply.query,
            "response": reply.response,
            "timestamp": reply.created_at.isoformat()
        } for reply in result   
    ]  

@app.get("/search")
def search_files(query:str, user:User = Depends(get_current_user), db:Session = Depends(SessionLocal)):
    files = db.query(File).filter(File.filename.ilike(f"%{query}%")).all()
    return files

