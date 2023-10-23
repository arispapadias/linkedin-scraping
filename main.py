from fastapi import FastAPI
from app import jobs

app = FastAPI()

@app.post("/items/")
async def insert_jobs(item: jobs.Jobs):
    return jobs.insert_jobs(item)

@app.get("/get_linkedin_jobs/")
async def scrape_jobs(job_title: str = Query(..., description="Job Title"), location: str = Query(..., description="Write your location"), posted_date: str = Query(..., description="Job posted date"), job_level: str = Query(..., description="What job level you are looking for?")):
    try:
        jobs = scrape_jobs(job_title, location, posted_date, job_level)
       
        return jobs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


