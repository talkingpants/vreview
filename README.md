# VReview

**VReview** is a full-stack vulnerability review platform that integrates Microsoft Defender vulnerability data with a custom review and remediation workflow. It supports ticket creation in ServiceDesk Plus (on-prem).

## 🧱 Tech Stack

- **Frontend**: Angular
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (via Docker)
- **Containerisation**: Docker & Docker Compose

## 🚀 Features

- Retrieves software vulnerabilities from Microsoft Defender API
- Allows selection of software for remediation
- Creates tickets in ManageEngine ServiceDesk Plus (on-prem)
- Clean Angular + Flask architecture with CORS support
- Dockerised for consistent local and production deployment

## 📦 Project Structure

```
vreview/
├── backend/       # Flask backend
├── frontend/      # Angular frontend
├── docker-compose.yml
└── README.md
```

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/talkingpants/vreview.git
   cd vreview
   ```

2. **Configure environment**
   - Edit `/backend/.env` with your API keys and DB credentials

3. **Run containers**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   - Frontend: [http://localhost:4200](http://localhost:4200)
   - Backend API: [http://localhost:5000](http://localhost:5000)

## 💪 Status

> Backend and frontend are scaffolded and connected.  
> Defender API and ServiceDesk Plus integration in progress.

---

Feel free to fork, contribute, or raise issues!
