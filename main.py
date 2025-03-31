from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import zipfile
import pandas as pd
import json
import os
import openai
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

client = openai.OpenAI(
    api_key=AIPROXY_TOKEN,
    base_url=OPENAI_BASE_URL
)

app = FastAPI()

@app.get("/")
def home():
    """Health check endpoint"""
    return {"message": "FastAPI is running on Vercel!"}

@app.get("/health")
def health_check():
    """Health check route to verify deployment"""
    return {"status": "ok"}

def process_uploaded_file(file: UploadFile):
    try:
        file_extension = file.filename.split('.')[-1].lower()

        if file_extension == "zip":
            with zipfile.ZipFile(BytesIO(file.file.read()), 'r') as zip_ref:
                zip_contents = zip_ref.namelist()
                for file_name in zip_contents:
                    if file_name.endswith(('.txt', '.csv', '.json', '.xlsx')):
                        with zip_ref.open(file_name) as extracted_file:
                            return process_extracted_file(extracted_file, file_name)
            raise HTTPException(status_code=400, detail="No readable files found in ZIP.")

        else:
            return process_extracted_file(file.file, file.filename)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def process_extracted_file(file, filename):
    ext = filename.split('.')[-1].lower()

    if ext == "txt":
        return file.read().decode("utf-8").strip()

    elif ext == "csv":
        df = pd.read_csv(file)
        return df.to_dict()

    elif ext == "json":
        return json.load(file)

    elif ext == "xlsx":
        df = pd.read_excel(file)
        return df.to_dict()

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

@app.post("/api/")
async def process_question(
    question: str = Form(None), file: UploadFile = File(None)
):
    try:
        if file:
            extracted_content = process_uploaded_file(file)
            if isinstance(extracted_content, str):  
                question = extracted_content
            else:
                raise HTTPException(status_code=400, detail="Uploaded file does not contain valid text.")

        if not question:
            raise HTTPException(status_code=400, detail="No valid question provided.")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )

        answer = response.choices[0].message.content.strip()
        answer = answer.split("\n")[-1].strip()  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")

    return JSONResponse(content={"answer": answer})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
