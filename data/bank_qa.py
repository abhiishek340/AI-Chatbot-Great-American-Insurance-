import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Load the large dataset
try:
    data_file = Path(__file__).parent / 'bank_qa_large.json'
    with open(data_file, 'r', encoding='utf-8') as f:
        BANK_QA_DATA = json.load(f)
    logger.info(f"Loaded {len(BANK_QA_DATA)} QA pairs")
except FileNotFoundError:
    logger.warning("Large dataset not found, generating new dataset...")
    from .bank_qa_generator import generate_dataset
    generate_dataset()
    with open(data_file, 'r', encoding='utf-8') as f:
        BANK_QA_DATA = json.load(f)
    logger.info(f"Generated and loaded {len(BANK_QA_DATA)} QA pairs")

def get_context_for_question(question: str) -> str:
    """
    Enhanced retrieval function using keyword matching and category detection.
    """
    question_lower = question.lower()
    
    # Initialize variables for best matches
    best_matches = []
    best_score = 0
    
    # Keywords for better matching
    keywords = question_lower.split()
    
    for qa_pair in BANK_QA_DATA:
        # Calculate score based on keyword matches
        q_text = qa_pair["question"].lower()
        score = sum(2 for keyword in keywords if keyword in q_text)
        
        # Bonus points for exact phrase matches
        for i in range(len(keywords)-1):
            phrase = " ".join(keywords[i:i+2])
            if phrase in q_text:
                score += 1
        
        # Keep track of best matches
        if score > best_score:
            best_score = score
            best_matches = [qa_pair["answer"]]
        elif score == best_score and score > 0:
            best_matches.append(qa_pair["answer"])
    
    if best_matches:
        # Return the most relevant answer or combine multiple relevant answers
        if len(best_matches) == 1:
            return best_matches[0]
        else:
            # Combine multiple relevant answers
            return "\n\nRelated Information:\n".join(best_matches[:2])
    
    return "I apologize, but I don't have specific information about that. Please contact Great American Bank customer service for accurate information." 