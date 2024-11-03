import random
import json
from itertools import product

# Updated templates with actual Great American Insurance Group information
TEMPLATES = {
    "insurance_products": {
        "questions": [
            "What {insurance_type} insurance products do you offer?",
            "Tell me about your {insurance_type} insurance coverage",
            "What's included in your {insurance_type} insurance?",
            "How can I get a quote for {insurance_type} insurance?",
            "What are the benefits of {insurance_type} insurance with Great American?"
        ],
        "types": [
            "property and casualty", "specialty", "commercial", "business",
            "alternative markets", "crop", "aviation", "ocean marine",
            "inland marine", "executive liability", "cyber risk", "environmental",
            "excess liability", "fidelity/crime", "public sector"
        ]
    },
    "services": {
        "questions": [
            "How do I {service_action} a {service_type}?",
            "What's the process for {service_action} a {service_type}?",
            "Can you help me {service_action} a {service_type}?",
            "I need assistance with {service_action} my {service_type}",
            "What are the requirements for {service_action} a {service_type}?"
        ],
        "actions": [
            "file", "submit", "report", "track", "update", "review",
            "manage", "access", "verify", "renew"
        ],
        "types": [
            "claim", "policy", "premium payment", "loss report",
            "coverage change", "risk assessment", "insurance certificate",
            "policy document", "insurance quote"
        ]
    },
    "specialty_divisions": {
        "questions": [
            "What does your {division} division cover?",
            "Tell me about Great American's {division} services",
            "What industries does your {division} division serve?",
            "How can I work with your {division} division?",
            "What solutions does your {division} division offer?"
        ],
        "types": [
            "Alternative Markets", "Aviation", "Bond", "Crop",
            "Environmental", "Excess Liability", "Executive Liability",
            "FCIA - Trade Credit & Political Risk", "Fidelity / Crime",
            "Ocean Marine", "Professional Liability", "Public Sector",
            "Specialty Equipment", "Specialty Human Services"
        ]
    }
}

# Generate answer templates
def generate_answer_template(category, type_value, action_value=None):
    answers = {
        "insurance_products": {
            "property and casualty": """Great American Insurance Group's Property and Casualty coverage includes:

1. Key Features:
   - Comprehensive property protection
   - Tailored casualty coverage
   - Industry-specific solutions
   - Risk management services

2. Coverage Options:
   - Property damage protection
   - Business interruption coverage
   - General liability
   - Workers' compensation
   - Commercial auto

3. Benefits:
   - Financial strength rating of "A+" (Superior) by A.M. Best
   - Specialized underwriting expertise
   - Dedicated claims handling
   - Risk engineering services

Contact our specialists at 1-800-545-4269 or visit our website to learn more.""",
            
            "specialty": """Great American's Specialty Insurance solutions provide:

1. Specialized Coverage:
   - Industry-specific protection
   - Customized policy options
   - Flexible coverage limits
   - Risk management expertise

2. Key Markets:
   - Professional services
   - Healthcare organizations
   - Financial institutions
   - Technology companies
   - Nonprofit organizations

3. Advantages:
   - Expert underwriting
   - Specialized claims handling
   - Risk management resources
   - Industry-leading coverage forms

Visit www.greatamericaninsurancegroup.com/specialty for detailed information.""",
            # Add more specific product descriptions
        },
        
        "services": f"""To {action_value} a {type_value} with Great American Insurance Group:

1. Process Steps:
   - Log in to your account at www.greatamericaninsurancegroup.com
   - Navigate to {type_value} section
   - Follow the guided process
   - Submit required documentation

2. Requirements:
   - Policy number
   - Account credentials
   - Relevant documentation
   - Contact information

3. Support Options:
   - Online portal assistance
   - Phone support: 1-800-545-4269
   - Email: claims@gaig.com
   - Local agent assistance

For immediate assistance, contact our customer service team.""",
        
        "specialty_divisions": {
            "Alternative Markets": """Great American's Alternative Markets Division specializes in:

1. Program Business:
   - Custom insurance programs
   - Industry-specific solutions
   - Captive insurance arrangements
   - Risk retention groups

2. Target Markets:
   - Professional associations
   - Industry groups
   - Large organizations
   - Specialty programs

3. Services:
   - Program development
   - Risk management
   - Claims handling
   - Administrative support

Contact our Alternative Markets team for specialized solutions."""
            # Add more division-specific responses
        }
    }
    
    # Get the appropriate response based on category and type
    if category == "specialty_divisions":
        return answers.get(category, {}).get(type_value, "Please contact our specialty divisions directly for specific information.")
    elif category == "insurance_products":
        return answers.get(category, {}).get(type_value, "Please contact our insurance specialists for specific product information.")
    else:
        return answers.get(category, "Please contact Great American Insurance Group for accurate information.")

def generate_dataset(output_file='bank_qa_large.json'):
    dataset = []
    
    # Generate variations for each category
    for category, data in TEMPLATES.items():
        questions = data['questions']
        
        if category == 'services':
            # Combine actions and types for services
            for q_template in questions:
                for action, type_value in product(data['actions'], data['types']):
                    question = q_template.format(
                        service_action=action,
                        service_type=type_value
                    )
                    answer = generate_answer_template(category, type_value, action)
                    dataset.append({"question": question, "answer": answer})
        else:
            # Generate for accounts and products
            for q_template in questions:
                for type_value in data['types']:
                    question = q_template.format(
                        account_type=type_value if category == 'accounts' else '',
                        product_type=type_value if category == 'products' else ''
                    )
                    answer = generate_answer_template(category, type_value)
                    dataset.append({"question": question, "answer": answer})
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)
    
    return len(dataset)

if __name__ == "__main__":
    count = generate_dataset()
    print(f"Generated {count} QA pairs") 