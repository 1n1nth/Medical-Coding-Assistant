# Medical Coding Assistant
A straightforward tool that takes medical text and suggests relevant ICD codes. Uses sentence embeddings and vector search to find matches based on semantic similarity rather than exact keyword matching.
The system processes natural language descriptions of medical conditions and returns ranked ICD code suggestions with confidence scores. It's built around a pre-trained sentence transformer model and FAISS for efficient similarity search across the code database.

# What It Does
Enter disease name or its symptoms and it returns a ranked list of ICD codes that match the description. The matching is done through semantic similarity - it understands that "chest pain" and "thoracic discomfort" are related concepts, not just exact string matches.
The application processes the input text, converts it to embeddings, and searches through a pre-indexed database of ICD codes to find the most semantically similar matches. Results include the ICD code, full description, and a similarity score.

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/medical-coding-app.git
cd medical-coding-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Download Data Files
The application requires 3 data files (~227MB total) that are stored separately due to GitHub size limits.

**Option A: Automatic Download (Recommended)**
```bash
python setup.py
```

**Option B: Manual Download**
If the automatic download fails, manually download these files to the `data/` folder:
- [cleaned_icd.csv](https://drive.google.com/file/d/1XJGQaZ6yd1_m8SZrS6bNfu5Hoh4Q-mQl/view) - ICD code database
- [description_embeddings.npy](https://drive.google.com/file/d/1D_y0axQL-XtxKYmjOZjFG9PPxFbdUwJn/view) - Pre-computed embeddings  
- [icd_index.faiss](https://drive.google.com/file/d/1Ud0m_cC5hHvxrhGE6BthU3FKAH1u1B2_/view) - FAISS search index

### 4. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure
```
medical-coding-app/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── setup.py              # Data download script
├── data/                 # Data files (downloaded separately)
│   ├── cleaned_icd.csv
│   ├── description_embeddings.npy
│   └── icd_index.faiss
├── models/
│   └── coding.py         # Medical coder class
├── static/
│   └── style.css         # Web interface styling
└── templates/
    └── index.html        # Web interface template
```

## Usage

1. Enter medical text in the textarea (e.g., "patient has chest pain and shortness of breath")
2. Select the number of results you want (3, 5, or 10)
3. Click "Find Matching Codes" to get ICD code suggestions
4. Review the suggested codes with their descriptions and match scores

## Technical Details

- **NLP**: spaCy for text preprocessing and entity extraction
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2) for semantic encoding
- **Search**: FAISS for efficient similarity search
- **Web Framework**: Flask for the user interface
- **Data**: ICD code database with pre-computed embeddings

## Data Files Information

The data files contain:
- **cleaned_icd.csv**: Processed ICD code database with descriptions
- **description_embeddings.npy**: Pre-computed sentence embeddings for all descriptions
- **icd_index.faiss**: FAISS index for fast vector similarity search

These files are generated from the original ICD code dataset and optimized for semantic search.

## Troubleshooting

**Data Download Issues:**
```bash
# Verify all files are present
python setup.py verify

# Re-download missing files
python setup.py
```

**Spacy Model Issues:**
```bash
python -m spacy download en_core_web_sm
```

**Import Errors:**
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Always consult with qualified medical professionals for actual medical coding decisions.
