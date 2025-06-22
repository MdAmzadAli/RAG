from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from cloudinary.uploader import upload
from cloudinary.exceptions import Error
import cloudinary
from parser import parse_file
from vector_store import upsert_to_qdrant
from models import File as DBFile
from dependencies import get_current_user
from helper.generate_uuid import generate_uuid
from Database.db_session import get_db
from embeddings import embedding_model
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

os.makedirs("temp", exist_ok=True)  

@router.post("/upload")
def upload_to_cloudinary(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    temp_path = f"temp/{file_id}_{file.filename}"
    try:
        
        file_id=generate_uuid()
        with open(temp_path, "wb") as f:
          f.write(file.file.read())

        chunks = parse_file(temp_path)
        vectors = embedding_model.embed_documents(chunks)
        upsert_to_qdrant(vectors, chunks, current_user.id, file_id)
        result = upload(file.file, resource_type="auto")
        new_file = DBFile(
            id=file_id,
            filename=file.filename,
            url=result["secure_url"],
            user_id=current_user.id
        )
       
        db.add(new_file)
        db.commit()

        return {"message": "File uploaded to Cloudinary","file_id": file_id ,"file_url": result["secure_url"]}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
          os.remove(temp_path)
