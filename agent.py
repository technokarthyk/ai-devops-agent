import ollama
import os
import subprocess
import yaml

# Ask user request
request = input("What pipeline do you want? ")

# Ask LLM to generate pipeline
response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": f"""
You are a DevOps engineer.

Generate a GitHub Actions CI/CD pipeline YAML.

User request: {request}

STRICT RULES:
- Return ONLY valid YAML
- Do NOT include explanations
- Do NOT include markdown like ```yaml
- Do NOT include comments outside YAML
"""
        }
    ]
)

pipeline = response["message"]["content"]

# Clean markdown if model adds it
pipeline = pipeline.replace("```yaml", "").replace("```", "").strip()

print("\nGenerated Pipeline:\n")
print(pipeline)

# Validate YAML
try:
    yaml.safe_load(pipeline)
    print("\nYAML validation successful")
except yaml.YAMLError as e:
    print("\nYAML validation failed:", e)
    exit()

# Create GitHub workflow directory
os.makedirs(".github/workflows", exist_ok=True)

# Save pipeline
pipeline_path = ".github/workflows/pipeline.yml"

with open(pipeline_path, "w") as f:
    f.write(pipeline)

print(f"\nPipeline saved to {pipeline_path}")

# Configure git user (if not configured)
subprocess.run('git config --global user.email "ai-devops-agent@example.com"', shell=True)
subprocess.run('git config --global user.name "AI DevOps Agent"', shell=True)

# Commit and push
subprocess.run("git add .", shell=True)
subprocess.run('git commit -m "AI generated CI/CD pipeline"', shell=True)
subprocess.run("git push", shell=True)

print("\nPipeline pushed to GitHub successfully 🚀")