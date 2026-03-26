from crewai import Agent, Task
# from ..llm import get_llm

contact_finder = Agent(
    role="Contact Information Finder",
    goal="Find business contact details from public sources",
    backstory="""
    You specialize in extracting phone numbers, emails, WhatsApp numbers
    from websites, directories, and listings.
    """,
    llm="gemini/gemini-2.5-flash",
    verbose=True
)

def contact_task(profile):

    return Task(
        description=f"""
        Using the business profile:

        {profile}

        Find:
        - Phone number
        - Email
        - WhatsApp (if available)
        - Source URL

         Return ONLY JSON:

        {{
            "phone": "...",
            "email": "...",
            "whatsapp": "...",
            "source": "..."
        }}

        If not found, use null.
        """,
        expected_output="Valid JSON contact card",
        agent=contact_finder,
    )
