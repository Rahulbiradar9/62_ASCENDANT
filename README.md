# Security Scan Project

A comprehensive security testing setup that combines OWASP ZAP automated scanning with a vulnerable target application for testing purposes.

## Prerequisites

- Node.js (v14 or higher)
- Python 3.7+
- Docker and Docker Compose
- Modern web browser with MetaMask extension

## Installation

1. Install project dependencies:
```bash
npm install
```

2. Install Python dependencies:
```bash
pip install python-owasp-zap-v2.4 requests
```

Start ZAP:
```bash
docker-compose up -d
```
Execute the security scan:
```bash
python3 scripts/zap_scan.py
```
Use different terminal:
```bash
docker-compose -f target-app/docker-compose.yml up -d
```
Update target_url in zap_scan.py to http://localhost:3000.

# ⚙️ Technology Stack

---

## 🎨 Frontend
<p align="left">
  <img src="https://img.shields.io/badge/React.js-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/MetaMask-E2761B?style=for-the-badge&logo=metamask&logoColor=white"/>
</p>

- **React.js** → Component-based, scalable UI development  
- **TypeScript** → Type safety for maintainable and robust code  
- **MetaMask** → Blockchain wallet integration for Web3 features  

---

## 🖥️ Backend
<p align="left">
  <img src="https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

- **Python 3** → API handling, backend logic, and integration  

---

## 🤖 Artificial Intelligence
<p align="left">
  <img src="https://img.shields.io/badge/Gemini_2.5_Pro-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google_AI_Studio-34A853?style=for-the-badge&logo=google&logoColor=white"/>
</p>

- **Gemini 2.5 Pro** → Advanced reasoning and AI-powered decision making  
- **Google AI Studio** → AI model building, testing, and deployment  

---

## 🛠️ DevOps & Security
<p align="left">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/OWASP_ZAP-000000?style=for-the-badge&logo=owasp&logoColor=white"/>
</p>

- **Docker** → Containerization for consistent and portable deployments  
- **OWASP ZAP** → Security testing and vulnerability scanning  

---

✅ With this stack, our solution is **scalable, secure, and AI-driven**, designed to meet real-world challenges in a hackathon setting.
