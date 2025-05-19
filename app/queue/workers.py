from ..db.collections.files import files_collection
from bson import ObjectId
import os
from pdf2image import convert_from_path
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_file(id: str, file_path: str):
    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "processing"
        }
    })

    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "converting to images"
        }
    })

    # Step1: Convert the PDF - Image
    pages = convert_from_path(file_path)
    images = []

    for i, page in enumerate(pages):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        images.append(image_save_path)

    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "converting to images successs"
        }
    })

    images_base64 = [encode_image(img) for img in images]

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are an expert resume reviewer. Given the following resume image, "
                            "analyze it and return your critique and suggestions for improvement in "
                            "the following format (no code block, just plain text):\n\n"
                            "Here's a detailed critique and suggestions for improvement based on the "
                            "provided resume:\n\n"
                            "What’s Good:\n\n"
                            "<bullet points for strengths>\n\n"
                            "What Can Be Improved & Mistakes Noted:\n\n"
                            "<numbered and bulleted list of issues, grouped by section as in the example>\n\n"
                            "Summary Table\nSection\tSuggestions/Errors\n<summary table as in the example>\n\n"
                            "In summary:\n<short summary paragraph>\n\n"
                            "Use clear headings, bullet points, and a summary table as shown. "
                            "Do not return a Python dictionary or code block."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{images_base64[0]}"
                        }
                    }
                ]
            }
        ]
    )

    await files_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "status": "processed",
            "result": response.choices[0].message.content
            if response.choices else "No response"
        }}
    )

