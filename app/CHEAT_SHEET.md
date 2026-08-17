# DevSecOps Project — Interview Cheat Sheet

## 1. What the project is
- Small **FastAPI** web app (Python)
- + a **CI/CD pipeline** on **GitHub Actions** that auto-checks security
- CI/CD = automatic test + ship on every code update, no human needed

## 2. The App
- **FastAPI** = framework to build the API endpoints
- `GET /health` → answers `{"status":"ok"}` = "I'm alive"
- `POST /login` → checks username/password → issues a **JWT** (stamped wristband)
- **JWT (PyJWT)** = signed token that proves you're logged in
- **Passlib** = passwords stored **hashed/scrambled**, never plain text
- **Pydantic** = validates incoming request data (comes with FastAPI)

## 3. Docker
- **Dockerfile** = recipe to build the image
- **python:3.11-slim** = tiny clean base image
- Image = sealed lunchbox → runs the same on any computer
- Runs as **non-root user** = less damage if hacked

## 4. GitHub + GitHub Actions
- **GitHub** = cloud code warehouse
- **main** = the official "finished" version
- **Push to main** = update the finished version
- **GitHub Actions** = robot that runs automatically on every push
- Workflow file: `.github/workflows/devsecops-pipeline.yml`

## 5. The 5 Gates (airport security for your code)
1. **Gate 1 – Setup**: checkout code + Python 3.11 ready
2. **Gate 2 – SAST (Bandit)**: reads the code, finds dangerous patterns → fails on HIGH
3. **Gate 3 – SCA (pip-audit)**: checks libraries vs known CVEs → fails on any CVE
4. **Gate 4 – Secrets (TruffleHog)**: sniffs code + git history for API keys/passwords → fails if any found
5. **Gate 5 – Container (Trivy)**: X-rays the Docker image → fails on CRITICAL/HIGH

**Any gate fails → RED → blocked. All pass → GREEN → "Security Verification Passed - Ready for Deployment"**

## 6. Key terms to know
- **SAST** = reading source code, looking for flaws (Bandit)
- **SCA** = checking third-party libraries for known vulnerabilities (pip-audit/Safety)
- **CVE** = public record of a known security flaw
- **Secret** = API key / password / token that must not be in code
- **Environment variable** = setting stored outside the code (JWT secret lives here)

## 7. Why 5 tools?
- Each checks a different layer:
  code → libraries → secrets → container image
- One tool cannot cover everything

## 8. 60-second answer
> "A small FastAPI app (health check + JWT login) packaged in Docker, with a DevSecOps GitHub Actions pipeline. On every push to main, 5 gates run: Bandit (SAST), pip-audit (SCA), TruffleHog (secret scanning), Trivy (container scanning). Any failure blocks deployment; all green prints 'Security Verification Passed.'"

## 9. Honesty rule
- If interviewer asks something deep you don't know → admit it's a learning project, explain what you DO know confidently.

---
### Endpoints memory trick
- `/health` = "are you open?"
- `/login` = "here's my ID, give me the wristband (JWT)"
