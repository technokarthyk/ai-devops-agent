import ollama
import os
import subprocess
import yaml

request = input("What pipeline do you want? ")

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": f"""
You are a DevOps engineer.

Generate a simple GitHub Actions workflow that prints
'Workflow ran successfully'.

Requirements:
- workflow name: Simple CI
- trigger on push to main branch
- also trigger on pull_request
- job name: success-job
- runner: ubuntu-latest
- use actions/checkout@v4
- print: Workflow ran successfully

Return ONLY valid YAML.
No explanations.
No markdown.
"""
        }
    ]
)

pipeline = response["message"]["content"]

pipeline = pipeline.replace("```yaml", "").replace("```", "").strip()

print("\nGenerated Pipeline:\n")
print(pipeline)

# Validate YAML
try:
    yaml.safe_load(pipeline)
    print("\nYAML validation successful")
except yaml.YAMLError as e:
    print("YAML validation failed:", e)
    exit()

# Create workflow directory
os.makedirs(".github/workflows", exist_ok=True)

workflow_file = ".github/workflows/pipeline.yml"

with open(workflow_file, "w") as f:
    f.write(pipeline)

print("Workflow saved.")

# Commit and push
subprocess.run("git add .", shell=True)
subprocess.run('git commit -m "AI generated workflow"', shell=True)
subprocess.run("git push", shell=True)

print("Workflow pushed to GitHub.")