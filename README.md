# 🔗 URL Shortener API

A production-ready URL Shortener REST API built with **FastAPI** and **PostgreSQL**. The application supports JWT authentication, URL shortening, QR code generation, click analytics, link expiration, rate limiting, and Docker deployment.

---

## 🚀 Features

* 🔐 User Registration & Login using JWT Authentication
* 🔗 Generate short URLs
* ↪️ Redirect to original URLs
* 📅 Optional link expiration
* 📊 Click analytics
* 📈 Last 7 days click statistics
* 📱 QR Code generation for every shortened URL
* ♻️ Duplicate URL handling
* 🚦 Rate limiting (SlowAPI)
* 🐳 Docker & Docker Compose support
* 📖 Interactive Swagger documentation

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT (python-jose)
* **Password Hashing:** Passlib (bcrypt)
* **QR Code:** qrcode
* **Rate Limiting:** SlowAPI
* **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

```
url-shortener/
│
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── static/
│   │   └── qr_codes/
│   ├── config.py
│   ├── database.py
│   ├── limiter.py
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/shortener_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BASE_URL=http://127.0.0.1:8000
```

---

## ▶️ Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd url-shortener
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Running with Docker

Build and start the application:

```bash
docker compose up --build
```

Stop the containers:

```bash
docker compose down
```

---

## 📚 API Endpoints

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| POST   | `/auth/register`          | Register a new user      |
| POST   | `/auth/login`             | Login and receive JWT    |
| POST   | `/links/`                 | Create a shortened URL   |
| GET    | `/r/{short_code}`         | Redirect to original URL |
| GET    | `/analytics/{short_code}` | View analytics           |
| GET    | `/health`                 | Health check             |

---

## 📊 Analytics

The analytics endpoint provides:

* Total number of clicks
* Original URL
* Link creator
* Click statistics for the last 7 days

---

## 📱 QR Code Generation

Every shortened URL automatically generates a QR code that can be scanned to access the shortened link.

---

## 🚦 Rate Limiting

To prevent abuse, redirect requests are rate-limited using SlowAPI. Exceeding the configured limit returns:

```
HTTP 429 Too Many Requests
```

---

## 📖 API Documentation

Interactive Swagger documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

## ✨ Future Improvements

* Custom aliases for shortened URLs
* User dashboard
* Link deletion
* Link editing
* Geographic analytics
* Redis caching

---

## 👩‍💻 Author

**Harsha K**
