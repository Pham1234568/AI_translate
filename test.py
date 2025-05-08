import yaml

with open(r'D:\CrewAI\crew\languageexport\src\languageexport\config\tasks.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)

print(data)
print("research_task" in data)
print(data["research_task"])