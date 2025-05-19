import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.title("AI-Powered Resume Reviewer")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], 
                               key="resume")
jd_file = st.file_uploader("Upload the job description (PDF)", type=["pdf"], 
                           key="jd")

if resume_file is not None and jd_file is not None:
    with st.spinner("Uploading..."):
        files = {
            "resume": (resume_file.name, resume_file, "application/pdf"),
            "jd": (jd_file.name, jd_file, "application/pdf"),
        }
        response = requests.post(f"{API_URL}/upload", files=files)
    if response.status_code == 200:
        file_id = response.json()["file_id"]
        st.success("Files uploaded! Processing...")

        status_placeholder = st.empty()
        result_placeholder = st.empty()

        # Poll for status
        while True:
            status_response = requests.get(f"{API_URL}/{file_id}")
            if status_response.status_code != 200:
                status_placeholder.error("Error fetching status.")
                break
            data = status_response.json()
            status = data["status"]
            status_placeholder.info(f"Status: {status}")

            if status == "processed" and data.get("result"):
                result_placeholder.markdown("### AI Feedback")
                result_placeholder.markdown(data["result"])
                break
            elif status in ["failed", "error"]:
                status_placeholder.error("Processing failed.")
                break
            time.sleep(2)
    else:
        st.error("Failed to upload files. Please try again.")

st.markdown("---")
st.caption("Powered by FastAPI backend and OpenAI/GPT-4 Vision")
