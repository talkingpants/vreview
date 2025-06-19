# VReview

**VReview** is a small vulnerability review platform. It pulls data from Microsoft Defender and helps create remediation tickets in ServiceDesk Plus.

## 🧱 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Static HTML served by Flask
- **Database**: PostgreSQL (via Docker)
- **Containerisation**: Docker & Docker Compose

## 🚀 Features

- Retrieves vulnerable software inventory from Microsoft Defender API
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
   - Set your Microsoft Defender credentials (`DEFENDER_TENANT_ID`,
     `DEFENDER_CLIENT_ID`, `DEFENDER_CLIENT_SECRET`) for API access

3. **Run containers**
   ```bash
   docker-compose up --build
   ```

   Alternatively, to run the backend without Docker, install dependencies and
   start the Flask server:

   ```bash
   pip install -r backend/requirements.txt
   python backend/run.py
   ```

4. **Access the app**
   - [http://localhost:5000](http://localhost:5000) serves the static frontend and API

## 💪 Status

Defender API integration is implemented for retrieving the vulnerable software inventory. ServiceDesk Plus integration is still in progress.

---

Feel free to fork, contribute, or raise issues!
