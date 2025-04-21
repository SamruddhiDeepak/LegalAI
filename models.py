from dotenv import load_dotenv
import os
import re
import google.generativeai as genai

# Load .env
load_dotenv()

# Get API key from environment
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

def clean_text(text):
    text = re.sub(r'\*+', '', text) 
    text = re.sub(r'^[-•]\s*', '', text, flags=re.MULTILINE)  
    return text.strip()

def classify_case_type(text) -> str:
    text_lower = text.lower()
    if "contract" in text_lower:
        return "Contract Dispute"
    elif "bail" in text_lower:
        return "Bail Application"
    elif "property" in text_lower:
        return "Property Dispute"
    elif "cheque" in text_lower:
        return "Cheque Bounce"
    return "General Legal Case"

def extract_facts(text):
    prompt = f"""
    Extract the following details from the given legal case text in bullet points:
    1. Parties involved (e.g., Plaintiff, Defendant)
    2. Main claim (e.g., breach of contract, personal injury)
    3. Key evidence mentioned (e.g., signed contract, emails)
    4. Important dates (e.g., contract date, hearing date)

    Legal Case Text:
    {text}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text
        return clean_text(response.text)
    except Exception as e:
        print(f"Error while extracting facts: {e}")
        return "Could not extract facts."

def apply_rules(facts, case_type):
    prompt = f"""
    Given the following facts and case type, provide:
    1. The exact legal outcome (e.g., judgment in favour of plaintiff/defendant)
    2. A brief explanation of the legal reasoning
    3. A confidence score between 0 and 100

    Case Type: {case_type}
    Facts:
    {facts}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        response_text = response.candidates[0].content.parts[0].text.strip()
        response_text = clean_text(response_text)

        outcome = reasoning = ""
        confidence = 70.0

        lines = response_text.splitlines()
        for line in lines:
            if "outcome" in line.lower():
                outcome = line.split(":", 1)[-1].strip()
            elif "reasoning" in line.lower():
                reasoning = line.split(":", 1)[-1].strip()
            elif "confidence" in line.lower():
                try:
                    confidence = float(re.findall(r'\d{1,3}\.?\d*', line)[0])
                except:
                    confidence = 70.0

        return outcome or "Outcome not found", reasoning or "Reasoning not available", confidence

    except Exception as e:
        print(f"Error while applying rules: {e}")
        return "Outcome Undecided", "Insufficient rule match", 50.0
