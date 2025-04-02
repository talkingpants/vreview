# VReview

**VReview** is a full-stack vulnerability review platform that integrates Microsoft Defender vulnerability data with a custom review and remediation workflow. It supports ticket creation in ServiceDesk Plus (on-prem).

## Tech Stack

- **Frontend**: Angular
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (via Docker)
- **Containerisation**: Docker & Docker Compose

## Features

- Retrieves software vulnerabilities from Microsoft Defender API
- Allows selection of software for remediation
- Creates tickets in ManageEngine ServiceDesk Plus (on-prem)
- Clean Angular + Flask architecture with CORS support
- Dockerised for consistent local and production deployment

## Project Structure

