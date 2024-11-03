from data.bank_qa_generator import generate_dataset
import os

def initialize():
    print("Initializing dataset...")
    # Create data directory if it doesn't exist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(current_dir, exist_ok=True)
    
    # Generate the dataset
    output_file = os.path.join(current_dir, 'bank_qa_large.json')
    count = generate_dataset(output_file)
    print(f"Generated {count} QA pairs")

if __name__ == "__main__":
    initialize() 