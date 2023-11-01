from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import JobModel, Jobs

DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_jobs(item):
    db = SessionLocal()
    db_job = JobModel(**item.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    db.close()
    return {"job": db_job}
    

async def find_job_description(job_link: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })
    resp = session.get(job_link)
    # print(resp.url)

    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")

    job_description = soup.find('div', class_='show-more-less-html__markup').text
    # <div class="jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch" id="job-details" tabindex="-1">
    # check if job_description is string var
    if isinstance(job_description, str):
        return job_description
    else:
        return {"no job description found"}
        

async def scrape_jobs(job_title, location, posted_date, job_level):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })
    resp = session.get(f"https://linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?kaywords={job_title}&location={location}&timePosted={posted_date}&jobLevel={job_level}")

    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}

    # Parse the HTML response and extract job listings and descriptions
    job_data = []

    try:
        job_listings = soup.find_all("li")
        # print(job_listings)

        for job_listing in job_listings:
            job_title = job_listing.find("h3", class_="base-search-card__title").text.strip()
            company_name = job_listing.find("h4", class_="base-search-card__subtitle").text.strip()
            company_location = job_listing.find("span", class_='job-search-card__location').text.strip()
            job_link = job_listing.find("a", class_="base-card__full-link").text.strip()

            job_description = await find_job_description(job_link)

            job_info = {
                "job_title": job_title,
                "company_name": company_name,
                "company_location": company_location,
                "job_description": job_description,
            }
            job_data.append(job_info)

        print(job_data)

        # save data to database

        insert_jobs(job_data)

        # db = SessionLocal()
        # for job_info in job_data:
        #     db_job = JobModel(**job_info)
        #     db.add(db_job)
        #     db.commit()
        #     db.close()

        return {'jobs': job_data}
    except KeyError:
        return {"error": "Unable to parse page"}
