from flask import Flask, render_template, request
from models.coding import MedicalCoder
import os
import sys
from pathlib import Path

app = Flask(__name__)

coder = None

def check_data_files():
    """Check if all required data files exist"""
    data_dir = Path("data")
    required_files = [
        "cleaned_icd.csv",
        "description_embeddings.npy", 
        "icd_index.faiss"
    ]
    
    missing_files = []
    for filename in required_files:
        if not (data_dir / filename).exists():
            missing_files.append(filename)
    
    return missing_files

def initialize_coder():
    global coder
    if coder is None:
        print("Checking for required data files...")
        
        # Check if data files exist
        missing_files = check_data_files()
        if missing_files:
            print(f"Missing data files: {', '.join(missing_files)}")
            print("Please run: python setup.py")
            print("This will download the required data files (~227MB)")
            sys.exit(1)
        
        print("Initializing medical coder...")
        try:
            coder = MedicalCoder(
                csv_path="data/cleaned_icd.csv",
                index_path="data/icd_index.faiss",
                embeddings_path="data/description_embeddings.npy"
            )
            print("Ready to serve requests!")
        except Exception as e:
            print(f"Error initializing medical coder: {e}")
            print("Please check that all data files are valid and complete.")
            sys.exit(1)

@app.route("/", methods=["GET", "POST"])
def home():
    # Ensure coder is initialized
    initialize_coder()
    
    results = []
    input_text = ""
    
    if request.method == "POST":
        input_text = request.form.get("medical_text", "")
        if input_text:
            try:
                top_n = int(request.form.get("top_n", "10"))
                results = coder.suggest_codes(input_text, top_n)
            except Exception as e:
                print(f"Error processing request: {e}")
                # You could add error handling to show user-friendly messages
                results = []
    
    return render_template("index.html", results=results, input_text=input_text)

@app.route("/health")
def health_check():
    """Simple health check endpoint"""
    missing_files = check_data_files()
    if missing_files:
        return {
            "status": "error", 
            "message": f"Missing data files: {', '.join(missing_files)}"
        }, 500
    
    return {"status": "healthy", "message": "All systems operational"}

if __name__ == "__main__":
    # Check data files before starting
    missing_files = check_data_files()
    if missing_files:
        print("\n" + "="*50)
        print("SETUP REQUIRED")
        print("="*50)
        print(f"Missing data files: {', '.join(missing_files)}")
        print("\nTo download the required data files (~227MB), run:")
        print("    python setup.py")
        print("\nOr manually download from the links in README.md")
        print("="*50)
        sys.exit(1)
    
    # Initialize coder on startup
    initialize_coder()
    
    # Run the Flask app
    print("\nStarting Medical Coding Assistant...")
    print("Open your browser to: http://localhost:5000")
    app.run(debug=True)
