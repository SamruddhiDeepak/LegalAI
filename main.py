import os
import json
from sentence_transformers import SentenceTransformer, util
from utils import process_case_file, get_non_solvable_reasons
from zero_shot_test import classifycase
from agents import analyze_case

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load reference solvable cases
with open("reference_cases.json", "r") as f:
    ai_solvable_refs = json.load(f)

# Encode the reference cases for comparison
ref_embeddings = model.encode(ai_solvable_refs, convert_to_tensor=True)

def evaluate_solvability(text):
    case_embedding = model.encode(text, convert_to_tensor=True)
    scores = util.cos_sim(case_embedding, ref_embeddings)[0]
    max_score = scores.max().item()
    best_match = ai_solvable_refs[scores.argmax().item()]
    return {
        "solvable": max_score >= 0.6,
        "confidence": round(max_score * 100, 2),
        "matched_case": best_match
    }

def main():
    file_path = input("Enter the path to the case file: ")
    case_text = process_case_file(file_path)

    classification = classifycase(case_text)
    solvability_result = evaluate_solvability(case_text)

    print("\n--- Case Analysis Summary ---")
    print(f"Predicted Case Type        : {classification['labels'][0]}")
    print(f"Classification Confidence  : {round(classification['scores'][0]*100, 2)}%")
    print(f"AI Solvable                : {'Yes' if solvability_result['solvable'] else 'No'}")
    print(f"Solvability Confidence     : {solvability_result['confidence']}%")
    print(f"Matched Reference Case     : {solvability_result['matched_case']}")

    if solvability_result["solvable"]:
        print("\n--- Initiating AI Legal Case Resolution ---")
        result = analyze_case(case_text)

        print("\n🔎 AI Legal Case Analysis Result")
        print(f"\nCase Type       : {result['case_type']}")
        print(f"\nExtracted Facts :\n{result['facts']}")
        print(f"\nOutcome         : {result['outcome']}")
        print(f"\nLegal Reasoning :\n{result['reasoning']}")
        print(f"\nConfidence      : {result['confidence']}%")
    else:
        print("\n⚠️ AI cannot solve this case confidently.")
        reasons = get_non_solvable_reasons(case_text)
        print("Reasons:")
        for reason in reasons:
            print(f"- {reason}")

if __name__ == "__main__":
    main()
