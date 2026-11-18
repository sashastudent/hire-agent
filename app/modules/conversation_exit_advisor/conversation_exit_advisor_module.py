import os
from pathlib import Path
from dotenv import load_dotenv
from transformers import pipeline
from transformers.utils import logging

load_dotenv()   # read EXIT_ADVISOR_MODEL (and the other settings) from .env

logging.set_verbosity_error()

# project root: .../hire-agent  (this file is app/modules/conversation_exit_advisor/...)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# local folder (dev) or a Hugging Face Hub id 
MODEL_NAME = os.getenv("EXIT_ADVISOR_MODEL", "notebooks/models/qwen-exit-advisor-ft-more-data")
local_path = PROJECT_ROOT / MODEL_NAME
model_source = str(local_path) if local_path.exists() else MODEL_NAME
print(model_source)

# loaded ONCE, when the module is first imported
exit_pipe = pipeline("text-generation", model=model_source, device_map="auto")

LABELS = ["continue", "schedule", "end"]

SYSTEM_PROMPT = (
    "You are a recruiting assistant for a Python Developer position. "
    "Given the SMS conversation so far between a recruiter and a job candidate, "
    "decide the recruiter's next action: continue, schedule, or end. "
    "Respond with only the category."
)

def format_history(turns):
   """Same format as in training: 'Recruiter: ...' / 'Candidate: ...'"""
   if not turns:
       return "(no messages yet - conversation start)"
   return "\n".join(f"{t['speaker'].capitalize()}: {t['text']}" for t in turns)

def normalize(text):
    for label in LABELS:
        if label.lower() in text.lower():
            return label
    return "continue"   # safe default if the model answers something unexpected


def get_exit_decision(turns)-> str:
    """
    turns: [{"speaker": "recruiter" | "candidate", "text": "..."}, ...]
           the conversation so far, ending with the candidate's latest message
    returns: "continue" | "schedule" | "end"
    """
    messages = [
       {"role":"system", "content": SYSTEM_PROMPT},
       {"role":"user", "content": format_history(turns)}
    ]

    output = exit_pipe(messages, max_new_tokens=5, do_sample=False)

    return normalize(output[0]["generated_text"][-1]["content"])