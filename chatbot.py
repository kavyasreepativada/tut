from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Set your OpenAI API key, base URL, and model name.
openai.api_key = "sk-5raZzyz1g5eMWWPXRe-KNg"
openai.api_base = "https://chatapi.akash.network/api/v1"  # Replace with your actual base URL
model = "Meta-Llama-3-1-8B-Instruct-FP8"  # e.g., "gpt-4"

app = FastAPI()

# Define the request model for the API endpoint.
class Query(BaseModel):
    query: str

def process_query(user_query: str) -> str:
    """
    Process the user's query using OpenAI's Chat API.
    The system prompt restricts the conversation to gym, workout, 
    and health topics.
    """
    system_prompt = (
        "You are an expert assistant specialized in gym, workout, and health "
        "topics. Answer only questions related to fitness, exercise routines, "
        "nutrition for workouts, gym equipment, and overall health advice."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )
        # Extract and return the assistant's reply.
        # NOTE: Typically you'd use index 0 unless you specifically expect more.
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.post("/query")
def get_response(query: Query):
    """
    POST endpoint that accepts a query and returns the chatbot's response.
    """
    answer = process_query(query.query)
    return {answer}
