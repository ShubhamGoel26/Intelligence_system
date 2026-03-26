from crewai import Agent, Task
# from ..llm import get_llm

researcher = Agent(
    role="Business Research Specialist",
    goal="Create a structured profile of a company",
    backstory="""
    You are an expert at analyzing companies from web data.
    You extract business model, size signals, digital presence, and tools used.
    """,
    llm="gemini/gemini-2.5-flash",
    verbose=True
)

def research_task(company):
    scraped_text = company.get("scraped_text", "")
    return Task(
        description=f"""
        Research the company: {company['name']} located in {company['location']}.

        Use the following real website data:
        {scraped_text}

        Instructions:
        - Base your answer ONLY on the provided data
        - Do NOT hallucinate

        Return ONLY valid JSON:

        {{
            "name": "{company['name']}",
            "location": "{company['location']}",
            "description": "...",
            "size_signals": "...",
            "digital_presence": "...",
            "tools_used": "..."
        }}

        Do not add explanations.
        """,
        expected_output="Valid JSON business profile",
        agent=researcher,
    )