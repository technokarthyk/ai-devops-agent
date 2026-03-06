import ollama
import os
import subprocess
import yaml

# -----------------------------
# USER REQUEST
# -----------------------------
request = input("What pipeline do you want? ")

# -----------------------------
# CHECK GIT REPOSITORY
# -----------------------------
if not os.path.exists(".git"):
    print("No git repo found. Initializing git repository...")
    subprocess.run("git init", shell=True)

# -----------------------------
# CHECK GITHUB REMOTE
# -----------------------------
remote_check = subprocess.run(
    "git remote get-url origin",
    shell=True,
    capture_output=True,
    text=True
)

if remote_check.returncode != 0:
    repo_name = os.path.basename(os.getcwd())

    print(f"No remote repo found. Creating GitHub repo: {repo_name}")

    subprocess.run(
        f"gh repo create {repo_name} --public --source=. --remote=origin",
        shell=True
    )

# -----------------------------
# GENERATE PIPELINE USING AI
# -----------------------------
response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": f"""
You are a DevOps engineer.

Generate a simple GitHub Actions CI/CD pipeline YAML.

User request: {request}

STRICT RULES:
- Return ONLY valid YAML
- No explanations
- No markdown
"""
        }
    ]
)

pipeline = response["message"]["content"]

# Clean markdown if present
pipeline = pipeline.replace("```yaml", "").replace("```", "").strip()

print("\nGenerated Pipeline:\n")
print(pipeline)

# -----------------------------
# VALIDATE YAML
# -----------------------------
try:
    yaml.safe_load(pipeline)
    print("\nYAML validation successful")
except yaml.YAMLError as e:
    print("\nYAML validation failed:", e)
    exit()

# -----------------------------
# SAVE WORKFLOW
# -----------------------------
os.makedirs(".github/workflows", exist_ok=True)

pipeline_path = ".github/workflows/pipeline.yml"

with open(pipeline_path, "w") as f:
    f.write(pipeline)

print(f"\nPipeline saved to {pipeline_path}")

# -----------------------------
# CONFIGURE GIT USER
# -----------------------------
subprocess.run(
    'git config --global user.email "ai-devops-agent@example.com"',
    shell=True
)

subprocess.run(
    'git config --global user.name "AI DevOps Agent"',
    shell=True
)

# -----------------------------
# COMMIT CHANGES
# -----------------------------
subprocess.run("git add .", shell=True)

subprocess.run(
    'git commit -m "AI generated CI/CD pipeline"',
    shell=True
)

# -----------------------------
# PUSH TO GITHUB
# -----------------------------
push_result = subprocess.run("git push -u origin HEAD", shell=True)

if push_result.returncode == 0:
    print("\nPipeline pushed to GitHub successfully 🚀")
else:
    print("\nPush failed. Please check Git configuration.")