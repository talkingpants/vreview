# VReview

**VReview** is a small vulnerability review platform. It pulls data from Microsoft Defender and helps create remediation tickets in ServiceDesk Plus.

## 🧱 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Static HTML served by Flask
- **Database**: PostgreSQL (via Docker)
- **Containerisation**: Docker & Docker Compose

## 🚀 Features

- Retrieves software vulnerabilities from Microsoft Defender API
- Allows selection of software for remediation
- Creates tickets in ManageEngine ServiceDesk Plus (on-prem)
- Simple Flask architecture
- Dockerised for consistent local and production deployment

## 📦 Project Structure

```
vreview/
├── backend/       # Flask app and static frontend
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
   - Copy `/backend/.env.example` to `/backend/.env` and adjust values as needed

3. **Run containers**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   - [http://localhost:5000](http://localhost:5000) serves the static frontend and API

## 💪 Status

> Core backend is scaffolded. Defender API and ServiceDesk Plus integration are in progress.

---

Feel free to fork, contribute, or raise issues!
