from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
from .services.excel_reader import read_companies
from .agents.crew import run_pipeline
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor


def run_pipeline_safe(company):
    try:
        return run_pipeline(company)
    except Exception as e:
        return {
            "company": company.get("name"),
            "error": str(e)
        }


async def process_companies(companies):

    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [
            loop.run_in_executor(executor, run_pipeline_safe, company)
            for company in companies
        ]

        results = await asyncio.gather(*tasks)

    return results


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://intelligence-system-theta.vercel.app"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/upload")
async def upload_file(file: UploadFile=File(...)):

    # file_path = f"temp/{file.filename}"
    #
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    # ✅ Ensure temp folder exists
    os.makedirs("temp", exist_ok=True)

    file_path = f"temp/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    companies = read_companies(file_path)
    # PARALLEL EXECUTION
    results = await process_companies(companies)

    # results = []
    #
    # for company in companies:
    #     try:
    #         result = run_pipeline(company)
    #         results.append(result)
    #     except Exception as e:
    #         results.append({
    #             "company": company["name"],
    #             "error": str(e)
    #         })

    return {"results": results}
