import re

def process_case_file(file_path):
    """Reads the case file and returns its text content."""
    with open(file_path, 'r') as file:
        return file.read()
    
# Keywords related to different types of non-solvable cases
NON_SOLVABLE_KEYWORDS = {
    "complexity": ["multi-party", "jurisdiction", "conflict of laws", "international", "cross-border", "complex legal theories"],
    "ambiguity": ["unclear", "uncertainty", "ambiguous", "incomplete evidence", "lack of clarity"],
    "subjectivity": ["subjective", "personal opinion", "discretion", "belief", "perception", "interpretation"],
    "human judgment": ["emotional", "mental health", "sentiment", "intuition", "moral", "ethical"],
    "specialized expertise": ["medical", "financial", "tax", "patent", "scientific", "expert testimony", "consultation"],
    "confidentiality": ["confidential", "sealed", "privileged", "classified", "sensitive information"],
    "legal precedence": ["case law", "precedent", "jurisprudence", "legal opinion"],
    "non-legal matters": ["personal disputes", "family matters", "emotional distress", "relationship conflicts"]
}

def get_non_solvable_reasons(case_text):
    reasons = []

    # Check for complexity
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["complexity"]):
        reasons.append("The case involves complex legal theories or multi-party disputes, which require detailed human analysis and legal expertise.")

    # Check for ambiguity
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["ambiguity"]):
        reasons.append("The case contains unclear or incomplete evidence, making it difficult to derive a definitive AI-based conclusion.")

    # Check for subjectivity
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["subjectivity"]):
        reasons.append("The case requires subjective judgment, which is outside the scope of AI, as it involves personal opinions or beliefs.")

    # Check for human judgment
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["human judgment"]):
        reasons.append("The case requires human intuition or moral judgment, which AI is not capable of processing effectively.")

    # Check for specialized expertise
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["specialized expertise"]):
        reasons.append("The case involves specialized fields such as medical, financial, or scientific expertise, requiring professionals in those fields.")

    # Check for confidentiality issues
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["confidentiality"]):
        reasons.append("The case involves confidential or privileged information that cannot be processed by AI due to privacy concerns.")

    # Check for legal precedence
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["legal precedence"]):
        reasons.append("The case involves intricate legal precedents or case law, which requires interpretation by a legal expert.")

    # Check for non-legal matters
    if any(keyword in case_text.lower() for keyword in NON_SOLVABLE_KEYWORDS["non-legal matters"]):
        reasons.append("The case pertains to personal, emotional, or family-related issues, which AI cannot resolve as they require human empathy and legal context.")

    # If no match was found, provide a generic reason
    if not reasons:
        reasons.append("The case is outside the scope of AI-driven resolution due to its unique or complex nature.")

    return reasons


