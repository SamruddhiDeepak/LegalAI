from models import extract_facts, apply_rules
from models import classify_case_type, extract_facts, apply_rules


def analyze_case(text):
    case_type = classify_case_type(text)  
    
    facts = extract_facts(text)
    
    outcome, reasoning, confidence = apply_rules(facts, case_type)
    
    return {
        "case_type": case_type,
        "outcome": outcome,
        "reasoning": reasoning,
        "confidence": confidence
    }
