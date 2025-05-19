from ..db.collections.files import files_collection
from bson import ObjectId
import os
from pdf2image import convert_from_path
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import pdfplumber

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def gemini_call(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text


async def process_file(id: str, resume_path: str, jd_path: str):
    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "processing"}})

    resume_text = extract_text_from_pdf(resume_path)
    jd_text = extract_text_from_pdf(jd_path)

    def rewrite_jd_node(inputs):
        prompt = (
            "Rewrite the following job description to make it more clear and "
            "effective:\n\n" + inputs['jd_text']
        )
        rewritten_jd = gemini_call(prompt)
        return {
            "rewritten_jd": rewritten_jd,
            "resume_text": inputs["resume_text"]
        }

    def compare_resume_node(inputs):
        prompt = (
            f"Given this job description:\n{inputs['rewritten_jd']}\n\n"
            f"And this resume:\n{inputs['resume_text']}\n\n"
            "Analyze the resume against the job description. "
            "Extract the candidate's strengths, identify weaknesses or "
            "mismatches, and recommend areas of improvement."
        )
        analysis = gemini_call(prompt)
        return {"analysis": analysis}

    # Build LangGraph (fix: use StateGraph for recent langgraph versions)
    try:
        from langgraph.graph import StateGraph
        from typing import TypedDict
        class State(TypedDict):
            jd_text: str
            resume_text: str
            rewritten_jd: str
            analysis: str
        graph = StateGraph(state_schema=State)
        graph.add_node("rewrite_jd", rewrite_jd_node)
        graph.add_node("compare_resume", compare_resume_node)
        graph.add_edge("rewrite_jd", "compare_resume")
        graph.set_entry_point("rewrite_jd")
        result = graph.run({
            "jd_text": jd_text,
            "resume_text": resume_text
        })
    except (ImportError, AttributeError, ValueError, TypeError):
        # Fallback: run the workflow manually if StateGraph is not available
        node1 = rewrite_jd_node({"jd_text": jd_text, "resume_text": resume_text})
        node2 = compare_resume_node(node1)
        result = {"rewritten_jd": node1["rewritten_jd"], "analysis": node2["analysis"]}

    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "processed",
            "rewritten_jd": result["rewritten_jd"],
            "result": result["analysis"]
        }
    })

