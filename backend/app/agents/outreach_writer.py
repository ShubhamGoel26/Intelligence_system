from crewai import Agent, Task
# from ..llm import get_llm

outreach_writer = Agent(
    role="Sales Outreach Specialist",
    goal="Write high-converting cold outreach messages",
    backstory="""
    You write short, sharp WhatsApp-style messages that focus on outcomes.
    You represent Brokai Labs, an AI systems company.
    """,
    llm="gemini/gemini-2.5-flash",
    verbose=True
)

def outreach_task(profile, contact):

    return Task(
        description=f"""
        Write a WhatsApp-style outreach message.

        Company Profile:
        {profile}

        Contact Info:
        {contact}

        Constraints:
        - Keep it under 80 words
        - Outcome-first
        - Personalized
        - Friendly, not spammy

        Output only message text.
        """,
        expected_output="Final outreach message",
        agent=outreach_writer,
    )
