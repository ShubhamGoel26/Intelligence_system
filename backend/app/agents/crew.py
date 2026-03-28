import json
import re
from crewai import Crew
from .researcher import researcher, research_task
from .contact_finder import contact_finder, contact_task
from .outreach_writer import outreach_writer, outreach_task
from ..services.scraper import get_company_data


def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            return None


def run_pipeline(company):
    scraped_data = get_company_data(company["name"])
    # -------------------
    # STEP 1: RESEARCH
    # -------------------
    # task1 = research_task(company)
    task1 = research_task({
        **company,
        "scraped_text": scraped_data["raw_text"]
    })

    crew1 = Crew(
        agents=[researcher],
        tasks=[task1],
        verbose=True
    )

    result1 = crew1.kickoff()
    profile = safe_json_parse(result1)

    if not profile:
        profile = {
            "name": company["name"],
            "location": company.get("location"),
            "description": "Not found",
            "size_signals": None,
            "digital_presence": None,
            "tools_used": None
        }

    # -------------------
    # STEP 2: CONTACT
    # -------------------
    task2 = contact_task(profile)

    crew2 = Crew(
        agents=[contact_finder],
        tasks=[task2],
        verbose=True
    )

    result2 = crew2.kickoff()
    contact = {
        "phone": scraped_data["phones"][0] if scraped_data["phones"] else None,
        "email": scraped_data["emails"][0] if scraped_data["emails"] else None,
        "whatsapp": None,
        "source": scraped_data["source"]
    }
    if not contact["phone"] and not contact["email"]:
        task2 = contact_task(profile)

        crew2 = Crew(
            agents=[contact_finder],
            tasks=[task2],
            verbose=True
        )

        result2 = crew2.kickoff()
        contact = safe_json_parse(result2) or contact
    # contact = safe_json_parse(result2)

    # if not contact:
    #     contact = {
    #         "phone": None,
    #         "email": None,
    #         "whatsapp": None,
    #         "source": None
    #     }

    # -------------------
    # STEP 3: OUTREACH
    # -------------------
    task3 = outreach_task(profile, contact)

    crew3 = Crew(
        agents=[outreach_writer],
        tasks=[task3],
        verbose=True
    )

    message = crew3.kickoff()
    final_output = getattr(message, "raw", None) or getattr(message, "output", None) or str(message)

    # -------------------
    # FINAL STRUCTURE
    # -------------------
    return {
        "company": company["name"],
        "profile": profile,
        "contact": contact,
        "outreach_message": final_output
    }
