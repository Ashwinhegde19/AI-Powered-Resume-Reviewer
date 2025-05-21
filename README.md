# AI Powered Resume Roaster

A full-stack application that allows users to upload their resume (PDF) and a job description (JD), processes them using Google Gemini AI, and provides detailed feedback on strengths, weaknesses, and improvement suggestions. The backend is built with FastAPI, MongoDB, and Redis (Valkey), and the frontend is built with Streamlit.

---

## Features
- **Upload Resume & JD:** Upload your PDF resume and job description via a simple web interface.
- **AI Review:** The backend uses Google Gemini ("gemini-2.0-flash") to rewrite the JD, compare it to your resume, and provide actionable feedback in a detailed, human-readable format.
- **Status Tracking:** See the processing status in real time.
- **Feedback Display:** View AI-generated feedback, including markdown and tables, directly in the frontend.

---

## Tech Stack
- **Backend:** FastAPI, MongoDB, Redis (Valkey), RQ, Google Gemini API, LangGraph, pdfplumber
- **Frontend:** Streamlit
- **Containerization:** Docker Compose

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AI_Powered_Resume_Roaster
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add your Gemini API key:
```env
GEMINI_API_KEY=your-gemini-api-key
```

### 3. Start the Backend and Services
Use Docker Compose to start MongoDB, Redis (Valkey), and the dev container:
```bash
docker compose up -d
```

### 4. Install Python Dependencies
(Inside the dev container or your Python environment)
```bash
pip install -r requirements.txt
```

### 5. Run the FastAPI Backend
```bash
bash run.sh
```
The backend will be available at [http://localhost:8000](http://localhost:8000)

### 6. Run the Streamlit Frontend
In a new terminal:
```bash
streamlit run streamlit_app.py
```
The frontend will be available at [http://localhost:8501](http://localhost:8501)

### 7. Start the RQ Worker (Required for Processing)
In another terminal (inside the dev container):
```bash
rq worker --with-scheduler --url redis://valkey:6379
```
This will process uploaded resumes and JDs in the background.

---

## MongoDB Compass Connection
To view your data in MongoDB Compass, use this connection string:
```
mongodb://admin:admin@localhost:27017/mydb?authSource=admin
```
- **Host:** `localhost`
- **Port:** `27017`
- **Username:** `admin`
- **Password:** `admin`
- **Auth DB:** `admin`
- **Database:** `mydb`

---

## File Storage
- Uploaded resumes and JDs are saved in `/mnt/uploads/<file_id>/<filename>` inside the app container.
- Example: `/mnt/uploads/682ad901098f8068ed612f77/resume_john_doe.pdf`
- All file metadata and AI results are stored in the MongoDB `files` collection.

---

## Usage
1. Open the Streamlit app in your browser.
2. Upload your PDF resume and job description.
3. Wait for processing (status will update automatically).
4. View detailed AI feedback and suggestions.

---

## Project Structure
```
AI_Powered_Resume_Roaster/
├── app/
│   ├── main.py
│   ├── server.py
│   ├── db/
│   ├── queue/
│   └── utils/
├── streamlit_app.py
├── requirements.txt
├── run.sh
├── docker-compose.yaml
└── README.md
```

---

## Branch Naming Conventions
- Use `feature/<short-description>` for new features (e.g., `feature/jd-resume-comparison`).
- Use `bugfix/<short-description>` for bug fixes.
- Use `docs/<short-description>` for documentation updates.

## Troubleshooting
- **MongoDB/Redis connection errors:** Ensure Docker containers are running and accessible.
- **Gemini API errors:** Check your API key and usage limits for the selected provider.
- **File upload issues:** Ensure `/mnt/uploads/` is writable by the backend.
- **MongoDB Compass:** If you get `auth failed`, double-check your username, password, and `authSource=admin` in the connection string. If you get `getaddrinfo EAI_AGAIN mongo`, use `localhost` as the host.

---

## Optional & Future Improvements
- Further UI/UX improvements in Streamlit frontend
- More granular error handling
- User authentication
- File cleanup/retention policies
- Additional AI analysis features

## License
MIT License


