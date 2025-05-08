from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
import os
from languageexport.tools.custom_tool import SaveTranslationInput
import pandas as pd     
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
name_0="openrouter/tngtech/deepseek-r1t-chimera:free"
name_z="openrouter/google/gemini-2.5-pro-exp-03-25:free"
name="openai/gpt-4.1-mini-2025-04-14"
llm=LLM(
    model=name_0,
    temperature=0.0,
)
import yaml

@CrewBase
class LanguagesExport():
    def __init__(self):
        agents_config = yaml.safe_load(open(r'D:\CrewAI\crew\languageexport\src\languageexport\config\agents.yaml', encoding='utf-8'))
        tasks_config = yaml.safe_load(open(r'D:\CrewAI\crew\languageexport\src\languageexport\config\tasks.yaml', encoding='utf-8'))
    @agent
    def translator_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['translator_researcher'],
            llm=llm,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_pydantic=SaveTranslationInput,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.translator_researcher()],
            tasks=[self.research_task()],
            process=Process.sequential,
            verbose=True
        )