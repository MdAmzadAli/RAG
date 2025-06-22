After pulling the repo locally, Follow this steps:

1) Fill The Environment Variables 

- Create a ".env" file at root level inside of "backend" folder
- add this env variables listed below:
```env QDRANT_API_KEY= QDRANT_URL= DATABASE_URL= JWT_SECRET_KEY= CLOUDINARY_CLOUD_NAME= CLOUDINARY_API_KEY= CLOUDINARY_API_SECRET= OPENAI_API_KEY= ``` 

- Create a "config.json" file at root level inside backend folder
and add this piece of code in it:

[
  {
    "model": "gpt-4",
    "api_key": "Your OpenAI API Key"
  }
]

2) For "backend" folder (use sql database only)

- Open "backend" folder in your terminal
- run "pip install -r requirements.txt"
- run "python -m Database.init_db" to create database schema 
- run "uvicorn main:app --reload"

3) For "frontend" folder

- Open the "frontend" folder in terminal
- run "npm install"
- npm run dev



