# hire-agent

## Installation

Create a virtual environment and install the requirements:

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Environment configuration
Create the .env file and add necessary keys:
OPENAI_API_KEY - your openAI api key, if you don't have one create it here - https://platform.openai.com/api-keys
AUTH_MODE - the DB authentication mode: sql or windows authentication
USERNAME - DB user in case sql auth mode is used
PASSWORD - DB password in case sql auth mode is used

## Database setup

1. Run the `db_Tech.sql` script provided with the assignment. It creates the `Tech` database and the `Schedule` table, seeded with interview slots for **2024**.
2. After running the script, update the year of all the dates to **2026**, so the bot has current dates to offer:

   ```sql
   USE Tech;
   UPDATE Schedule SET date = DATEADD(YEAR, 2, date) WHERE YEAR(date) = 2024;
   ```

   Only the year changes. The availability of every slot (`available`), the times and the positions stay exactly as they were in the original script.

## Conversation Exit Advisor model

We took the `Qwen/Qwen2.5-0.5B-Instruct` model, fine-tuned it (LoRA) on our conversations, and uploaded it to the Hugging Face Hub:

https://huggingface.co/sashabestie/qwen-exit-advisor

To run the project, put the model in the `.env` file under the `EXIT_ADVISOR_MODEL` key:

```
EXIT_ADVISOR_MODEL=sashabestie/qwen-exit-advisor
```

The model is downloaded automatically from the Hub on the first run.

## Run the app

From the project folder, run:

```
python -m streamlit run streamlit_app/streamlit_main.py
```

The app opens in the browser (usually at http://localhost:8501).
