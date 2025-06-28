from flask import Flask, render_template, request
from models.coding import MedicalCoder
import os

app = Flask(__name__)

# Global variable to hold the coder instance
coder = None

def initialize_coder():
    global coder
    if coder is None:
        print("Initializing medical coder...")
        coder = MedicalCoder(
            csv_path=r"medical_coding_app\data\cleaned_icd.csv",
            index_path=r"medical_coding_app\data\icd_index.faiss",
            embeddings_path=r"medical_coding_app\data\description_embeddings.npy"
        )
        print("Ready to serve requests!")

@app.route("/", methods=["GET", "POST"])
def home():
    # Ensure coder is initialized
    initialize_coder()
    
    results = []
    input_text = ""
    
    if request.method == "POST":
        input_text = request.form.get("medical_text", "")
        if input_text:
            top_n = int(request.form.get("top_n", "10"))
            results = coder.suggest_codes(input_text, top_n)
    
    return render_template("index.html", results=results, input_text=input_text)

if __name__ == "__main__":
    # Initialize coder on startup
    initialize_coder()
    app.run(debug=True)