from crewai import Agent, Task, Crew
from crewai.project import agent
from crewai.tools import tool
from litellm import completion
from dotenv import load_dotenv
load_dotenv()
# Tools powered by LiteLLM
@tool("generation_tool")
def generation_tool(prompt: str) -> str:
    """
    Performs generation via LiteLLM
    Args:
      - prompt: user prompt to expand/transform
    Returns:
      - generated text (string)
    """
    resp = completion(
        model="sap/gemini-2.5-pro",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp["choices"][0]["message"]["content"]

@tool("paraphrase_tool")
def paraphrase_tool(text: str, style: str = "concise") -> str:
    """
    Paraphrases text in a given style via LiteLLM.
    Supported styles: 'concise' | 'formal' | 'casual'.
    """
    style_map = {
        "concise": "Be concise and to the point.",
        "formal": "Use a formal business tone.",
        "casual": "Use a friendly, casual tone.",
    }
    style_instr = style_map.get(style, style_map["concise"])

    resp = completion(
        model="sap/o3",
        messages=[
            {"role": "system", "content": style_instr},
            {"role": "user", "content": text},
        ],
    )
    return resp["choices"][0]["message"]["content"]

# Ask for the topic at runtime
topic = input("Enter the blog topic: ").strip() or "CrewAI"

# --- Define agents ---
researcher = Agent(
    role="Researcher (AI Expert)",
    goal=f"Conduct in-depth research on: {topic}. Produce a comprehensive, technically accurate digest with interesting facts, notable libraries, caveats, and references where possible.",
    backstory="You are a senior AI engineer and investigator who cross-checks claims and surfaces non-obvious insights.",
    llm="sap/gemini-2.5-pro",
    tools=[generation_tool],
    allow_delegation=False,
)

writer = Agent(
    role="Developer Advocate (Writer)",
    goal="Write an engaging blog note with a compelling title and two paragraphs, each 2–3 sentences, appealing to both technical and non-technical readers.",
    backstory="You are an experienced DevRel who translates complex technical findings into clear, engaging stories.",
    llm="sap/gpt-4o",
    tools=[paraphrase_tool, generation_tool],
    allow_delegation=False,
)

# --- Define tasks ---
research_task = Task(
    description=(
        f"Research the topic “{topic}”. Cover purpose, architecture/inner workings, common use cases, strengths, "
        f"limitations, related tools/libraries, real-world adoption, and at least 2 interesting or lesser-known facts. "
        f"Be specific and technically sound."
    ),
    expected_output=(
        "A thorough digest with 8–12 bullet points covering: purpose, architecture, use cases, strengths, "
        "limitations, related tools, adoption examples, and interesting facts. Include brief references or keywords where applicable."
    ),
    agent=researcher,
)

write_task = Task(
    description=(
        "Using the research results, write a short blog post intended for both engineers and general readers. "
        "Output format: a single engaging H1 title, followed by exactly two paragraphs (2–3 sentences each). "
        "Make it informative yet approachable; avoid jargon without explanation."
    ),
    expected_output="Markdown with exactly: one H1-level title and two paragraphs (2–3 sentences each). No extra sections.",
    agent=writer,
    context=[research_task],
)

# --- Assemble crew ---
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True,
)

# --- Run ---
result = crew.kickoff()
print("\n📘 Result:\n", result)