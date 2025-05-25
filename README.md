# discord-bot
The public repository for Airweave's discord bot.


# 🤖 Airweave Discord Bot

![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Production%20Ready-blue?style=for-the-badge&logo=docker)

> A modern, scalable Discord bot built with FastAPI, designed for seamless integration and high performance.

---

## 🚀 Overview

**Airweave Discord Bot** is a cutting-edge solution for integrating Discord interactions using FastAPI. It leverages the latest technologies to ensure scalability, maintainability, and adherence to best practices.

---


## 📁 Project Structure

```bash
airweave-discord-bot/
├── app/
│   ├── api/                # FastAPI route handlers
│   │   └── interactions.py # Discord interactions endpoint
│   ├── core/               # Core configurations and utilities
│   │   ├── config.py       # Pydantic settings management
│   │   └── verify_signature.py # Request signature verification
│   ├── services/           # Business logic and services
│   │   └── discord_service.py # Discord-related operations
│   ├── models/             # Pydantic models and database schemas
│   │   └── interaction.py  # Interaction data models
│   └── main.py             # Application entry point
├── tests/                  # Test cases
│   ├── __init__.py
│   └── test_interactions.py
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Getting Started

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/airweave-ai/airweave-discord-bot.git
cd airweave-discord-bot
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Setup .env file**

```.env
DISCORD_PUBLIC_KEY=your_discord_public_key
DISCORD_BOT_TOKEN=your_discord_bot_token
```