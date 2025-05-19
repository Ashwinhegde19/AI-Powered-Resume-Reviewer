# AI Powered Resume Reviewer

A full-stack application that allows users to upload their resume (PDF), processes it using AI (OpenAI GPT-4 Vision), and provides detailed feedback on improvements and mistakes. The backend is built with FastAPI, MongoDB, and Redis (Valkey), and the frontend is built with Streamlit.

---

## Features
- **Upload Resume:** Upload your PDF resume via a simple web interface.
- **AI Review:** The backend uses OpenAI's GPT-4 Vision to analyze your resume and provide actionable feedback.
- **Status Tracking:** See the processing status in real time.
- **Feedback Display:** View AI-generated feedback, including markdown and tables, directly in the frontend.

---

## Tech Stack
- **Backend:** FastAPI, MongoDB, Redis (Valkey), RQ, OpenAI API
- **Frontend:** Streamlit
- **Containerization:** Docker Compose

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AI_Powered_Resume_Reviewer
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-...
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
This will process uploaded resumes in the background.

---

## Usage
1. Open the Streamlit app in your browser.
2. Upload your PDF resume.
3. Wait for processing (status will update automatically).
4. View detailed AI feedback and suggestions.

---

## Project Structure
```
AI_Powered_Resume_Reviewer/
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

## Troubleshooting
- **MongoDB/Redis connection errors:** Ensure Docker containers are running and accessible.
- **OpenAI API errors:** Check your API key and usage limits.
- **File upload issues:** Ensure `/mnt/uploads/` is writable by the backend.

---

## License
MIT License
