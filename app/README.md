# DevSecOps Automated CI/CD Pipeline (GitHub Actions)

A lightweight, production-grade DevSecOps pipeline for a **Python (FastAPI)** web application.
Every push to `main` triggers **5 sequential security gates**. The pipeline is **green only
if every gate passes** — otherwise it blocks the deployment.

---

## Repository Structure

```plaintext
devsecops-pipeline/
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml   # The 5-gate DevSecOps pipeline
├── app/
│   ├── __init__.py
│   └── main.py                      # FastAPI app (/health, /login)
├── Dockerfile                       # python:3.11-slim
├── requirements.txt                 # Pinned, CVE-clean dependencies
└── README.md
```

## The Application

| Endpoint  | Method | Purpose                                  |
|-----------|--------|------------------------------------------|
| `/health` | `GET`  | Liveness probe, returns `{"status": "ok"}` |
| `/login`  | `POST` | Verifies credentials, returns a signed JWT |

Demo credentials: `admin` / `password` (password is stored as a `pbkdf2_sha256` hash).

Run it locally:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker build -t devsecops-app .
docker run -p 8000:8000 devsecops-app
```

---

## Pipeline Architecture & Tool Roles

```mermaid
graph LR
    A[Push to main] --> B[Gate 1: Checkout & Python 3.11]
    B --> C[Gate 2: SAST - Bandit]
    C --> D[Gate 3: SCA - pip-audit / Safety]
    D --> E[Gate 4: Secret Scanning - TruffleHog]
    E --> F[Gate 5: Container Scan - Trivy]
    F --> G[Security Verification Passed - Ready for Deployment]
    C -- high severity found --> X[Pipeline FAILS]
    D -- CVE found --> X
    E -- secret found --> X
    F -- CRITICAL/HIGH CVE found --> X
```

| Gate | Tool | Category | What it does | Failure policy |
|------|------|----------|--------------|----------------|
| 1 | GitHub Actions | CI setup | Checks out the code and provisions a Python 3.11 runner | - |
| 2 | **Bandit** | SAST | Static analysis of Python source (`app/`) for insecure patterns: hardcoded passwords, SQL injection, eval usage, unsafe deserialization, etc. | Fails on **HIGH** severity findings (`-lll`) |
| 3 | **pip-audit** (Safety alternative) | SCA | Resolves `requirements.txt` against the OSV database and reports known CVEs in third-party libraries. **Safety** does the same job using the pyup.io vulnerability database but requires an API key; `pip-audit` is fully open-source and key-free, so it is used here. | Fails on any known vulnerability |
| 4 | **TruffleHog** | Secret scanning | Scans the working tree and commit history for secrets, API keys, and hardcoded passwords using regex + entropy detection. | Fails on any detected secret |
| 5 | **Trivy** | Container security | Builds the Docker image, then scans it for OS package and Python dependency vulnerabilities, including issues in the base image layers. | Fails on **CRITICAL/HIGH** vulnerabilities |

The gates run **sequentially** — a failure in any gate aborts the job immediately, so a
secret leak or a CVE never reaches deployment.

---

## Passing Run — How to Get a Green Pipeline

1. **Create a GitHub repository** and push this folder:

   ```bash
   git init
   git add .
   git commit -m "Init DevSecOps pipeline"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```

2. Open **Actions** in your repository — the `DevSecOps Pipeline` workflow starts on the
   push to `main`.

3. Wait for the 5 gates to finish. A green run ends with:
   ```
   Security Verification Passed - Ready for Deployment
   ```

> **Tip:** the code in this repo is already clean: dependencies are pinned to CVE-free
> versions and no secrets are committed. The pipeline should pass out of the box.

---

## Intentional Failure Test — Prove Gate 4 Blocks Deployment

> **Prerequisite:** GitHub has been rate-limiting commit-history scans, so this proof uses
> the current working tree. TruffleHog scans both the tree and the full git history.

1. **Insert a fake secret** into `app/main.py`:

   ```python
   AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
   ```

2. Commit and push:

   ```bash
   git add app/main.py
   git commit -m "demo: intentionally leak a fake AWS key"
   git push origin main
   ```

3. Open the workflow run. Gates 1-3 pass, then **Gate 4 (TruffleHog)** fails with output
   similar to:
   ```
   Found result: Detected Hardcoded Password or Secret (High Entropy String)
   ```
   because `AKIA...` matches the AWS Access Key pattern.

4. The job is **red** and the final "Ready for Deployment" step never runs — **deployment is blocked**.

5. **Remove the fake key**, commit, and push again to see the pipeline go green.

---

## Security Verification Passed — Ready for Deployment

```bash
echo "Security Verification Passed - Ready for Deployment"
```

This final message is only printed when all 5 gates succeed. In a real workflow, you would
replace this step with your actual deployment job (e.g., push the image to a registry and
deploy), which is now **guarded by the full DevSecOps chain**.
