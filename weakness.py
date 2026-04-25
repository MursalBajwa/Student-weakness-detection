import streamlit as st
import pandas as pd
import json
from datetime import datetime
import re
import io
import fitz
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
# from langchain_ollama import OllamaLLM
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\MURSA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Create Test", page_icon="📚", layout="wide")

# Session state
if 'tests_db' not in st.session_state:
    st.session_state.tests_db = []

if 'current_test' not in st.session_state:
    st.session_state.current_test = {
        'test_name': '',
        'class_section': '',
        'questions_df': pd.DataFrame(columns=['Q_No', 'Topic', 'Question_Text', 'Marks']),
        'extracted_text': ''
    }

if 'show_editor' not in st.session_state:
    st.session_state.show_editor = False
    
    
# ==================== COURSE CONTENT ================
def get_outline(class_section, subject):
    course_outline = {

    9: {
        "physics": [
            "Physical Quantities and Measurements",
            "Kinematics",
            "Dynamics",
            "Turning Effect of Forces",
            "Work, Energy and Power",
            "Gravitation",
            "Properties of Matter",
            "Thermal Properties of Matter",
            "Magnetism",
            "Nature of Science"
        ],
        "chemistry": [
            "Introduction to Chemistry",
            "Structure of Atom",
            "Periodic Table and Periodicity",
            "Structure of Molecules",
            "Physical States of Matter",
            "Solutions",
            "Electrochemistry",
            "Chemical Reactivity"
        ],
        "biology": [
            "Introduction to Biology",
            "Solving a Biological Problem",
            "Biodiversity",
            "Cells and Tissues",
            "Cell Cycle",
            "Enzymes",
            "Bioenergetics",
            "Nutrition",
            "Transport",
            "Coordination and Control"
        ],
        "mathematics": [
            "Real Numbers",
            "Logarithms",
            "Sets and Functions",
            "Factorization and Algebraic Manipulation",
            "Linear Equations and Inequalities",
            "Trigonometry",
            "Coordinate Geometry",
            "Logic",
            "Similar Figures",
            "Graphs of Functions",
            "Loci and Construction",
            "Information Handling"
        ]
    },

    10: {
        "physics": [
            "Simple Harmonic Motion and Waves",
            "Sound",
            "Geometrical Optics",
            "Electrostatics",
            "Current Electricity",
            "Electromagnetism",
            "Basic Electronics",
            "Information and Communication Technology",
            "Atomic and Nuclear Physics"
        ],
        "chemistry": [
            "Chemical Equilibrium",
            "Acids, Bases and Salts",
            "Organic Chemistry",
            "Hydrocarbons",
            "Biochemistry",
            "Environmental Chemistry",
            "Water",
            "Chemical Industries"
        ],
        "biology": [
            "Gaseous Exchange",
            "Homeostasis",
            "Coordination and Control",
            "Support and Movement",
            "Reproduction",
            "Inheritance",
            "Man and His Environment",
            "Biotechnology",
            "Pharmacology"
        ],
        "mathematics": [
            "Quadratic Equations",
            "Theory of Quadratic Equations",
            "Variations",
            "Partial Fractions",
            "Sets and Functions",
            "Basic Statistics",
            "Introduction to Trigonometry",
            "Projection of a Side of Triangle",
            "Chords of a Circle",
            "Tangent to a Circle",
            "Practical Geometry",
            "Circle Measurement"
        ]
    },

    11: {   # 1st Year
        "physics": [
            "Measurements",
            "Vectors and Equilibrium",
            "Motion and Force",
            "Work and Energy",
            "Circular Motion",
            "Fluid Dynamics",
            "Oscillations",
            "Waves"
        ],
        "chemistry": [
            "Basic Concepts",
            "Atomic Structure",
            "Chemical Bonding",
            "States of Matter",
            "Chemical Energetics",
            "Chemical Equilibrium",
            "Reaction Kinetics"
        ],
        "biology": [
            "Introduction to Biology",
            "Biological Molecules",
            "Enzymes",
            "Cell Structure",
            "Variety of Life",
            "Kingdom Prokaryotae",
            "Kingdom Protista",
            "Kingdom Fungi",
            "Kingdom Plantae",
            "Kingdom Animalia"
        ],
        "mathematics": [
            "Number Systems",
            "Sets and Functions",
            "Matrices and Determinants",
            "Quadratic Equations",
            "Partial Fractions",
            "Sequences and Series",
            "Permutations and Combinations",
            "Binomial Theorem",
            "Trigonometry",
            "Trigonometric Identities",
            "Trigonometric Functions"
        ],
        "computer_science": [
            "Introduction to IT",
            "Data Representation",
            "Computer Architecture",
            "Operating Systems",
            "Programming Fundamentals",
            "Control Structures"
        ]
    },

    12: {   # 2nd Year
        "physics": [
            "Electrostatics",
            "Current Electricity",
            "Capacitance",
            "Electromagnetism",
            "Electromagnetic Induction",
            "Alternating Current",
            "Physics of Solids",
            "Electronics",
            "Modern Physics",
            "Atomic Spectra",
            "Nuclear Physics"
        ],
        "chemistry": [
            "Periodic Classification",
            "s-Block Elements",
            "p-Block Elements",
            "d-Block Elements",
            "Coordination Compounds",
            "Fundamental Principles of Organic Chemistry",
            "Hydrocarbons",
            "Alkyl Halides",
            "Alcohols and Phenols",
            "Aldehydes and Ketones",
            "Carboxylic Acids",
            "Macromolecules"
        ],
        "biology": [
            "Homeostasis",
            "Support and Movement",
            "Coordination and Control",
            "Reproduction",
            "Growth and Development",
            "Chromosomes and DNA",
            "Cell Cycle",
            "Biotechnology",
            "Evolution",
            "Ecosystem"
        ],
        "mathematics": [
            "Functions and Limits",
            "Differentiation",
            "Integration",
            "Differential Equations",
            "Complex Numbers",
            "Vectors",
            "Analytical Geometry",
            "Conic Sections"
        ],
        "computer_science": [
            "Advanced Programming",
            "File Handling",
            "Data Structures",
            "Databases",
            "Networking"
        ]
    }
}
    return course_outline.get(int(class_section.split('-')[0]), {}).get(subject.lower(), [])

# ==================== EXTRACTION ====================

def preprocess_image(image):
    """Simple but effective preprocessing"""
    if image.mode != 'L':
        image = image.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    # Denoise
    arr = np.array(image)
    denoised = cv2.fastNlMeansDenoising(arr, None, 10, 7, 21)
    return Image.fromarray(denoised)

def extract_text(file_bytes, file_type):
    """Extract text from PDF or Image"""
    if file_type == "application/pdf":
        # Try text extraction first
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = []
        for i, page in enumerate(doc):
            txt = page.get_text()
            if txt and txt.strip():
                text_parts.append(f"--- Page {i+1} ---\n{txt}")
        
        text = "\n\n".join(text_parts)
        
        # If little text, OCR the PDF pages
        if len(text.strip()) < 100:
            text_parts = []
            for i, page in enumerate(doc):
                mat = fitz.Matrix(400/72, 400/72)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                proc = preprocess_image(img)
                page_text = pytesseract.image_to_string(proc, config='--psm 6')
                if page_text.strip():
                    text_parts.append(f"--- Page {i+1} ---\n{page_text}")
            text = "\n\n".join(text_parts)
        
        doc.close()
        return text
    else:
        # Image OCR
        image = Image.open(io.BytesIO(file_bytes))
        proc = preprocess_image(image)
        return pytesseract.image_to_string(proc, config='--psm 6')


# ==================== LLM ====================

class QuestionAnalyzer:
    def __init__(self):
        # Initialize Groq client instead of Ollama
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        # self.llm = OllamaLLM(model="llama3.2:3b", temperature=0.1)
        # self.llm = OllamaLLM(model="mistral:7b-instruct-q4_0", temperature=0.1)
    
    def analyze(self, text_content, class_section, subject):
        subject_topics = get_outline(
        class_section=class_section,
        subject=subject
    )

        # Convert list into clean string
        topics_text = "\n".join(
            [f"- {topic}" for topic in subject_topics]
        ) if subject_topics else "No predefined topics available"
        prompt = f"""
You are the best question paper analyzer in the world who does not make any mistake.Now, You are analyzing OCR/extracted text from a question paper for class {class_section} and subject {subject}.

The paper may contain:
- only MCQs
- only short questions
- only long questions
- a mix of MCQs, short questions, and long questions
- fill in the blanks
- true/false
- definitions
- numerical questions
- descriptive questions
- custom teacher-created sections

Important:
Question sections may have ANY heading style such as:
- Part A / Part B
- Section 1 / Section 2
- Objective
- Subjective
- Very Short Questions
- Descriptive Questions
- Essay Questions
- OR any custom heading

Do NOT rely on specific section names.
Do NOT rely on words like:
- any
- attempt
- answer

Instead:
- detect actual questions based on structure
- numbering patterns
- bullet patterns
- option patterns
- repeated formatting
- visible question statements

The extracted text may contain:
- random characters
- OCR mistakes
- broken words
- merged words
- missing spaces
- extra symbols
- mixed English and another language
- page headers/footers
- watermarks
- repeated labels
- noise from scanning

Your job:
- Remove random characters mentally.
- Reconstruct intended English words using context.
- Prefer English meaning if text is mixed-language.
- Ignore noise and unreadable garbage.
- Do NOT skip questions because numbering is wrong, missing, duplicated, or noisy.
- Do NOT miss any question.
- Keep questions in original order.
- If a question is split across multiple lines, merge it properly.
- Include MCQ options inside Question_Text if present.
- Do not merge multiple different questions into one.
- Do not create questions that do not exist.

Analyze this question paper using these subject outline topics:
{topics_text}

Topic rules:
- Match each question with the best topic from the outline
- If unclear, choose the closest valid topic
- Never leave topic empty

Marks rules:
- Use marks if explicitly written
- If section structure clearly defines marks, use that
- If marks are unclear, infer the most likely marks based on question structure and length
- Ignore random OCR numbers
- Do not assign random marks

Return ONLY JSON array:
[
  {{
    "Q_No": 1,
    "Topic": "detected topic",
    "Question_Text": "clean text",
    "Marks": 5
  }}
]

Content:
{text_content}

JSON:
"""
        
        try:
            # Call Groq API instead of Ollama
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are the best question paper analyzer in the world who does not make any mistake and a precise JSON generator. Return ONLY valid JSON arrays, no extra text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent JSON output
                max_tokens=8192   # Enough for detailed question analysis
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            
            # Find JSON array in response
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if match:
                data = json.loads(match.group())
                return pd.DataFrame([
                    {
                        'Q_No': int(item['Q_No']),
                        'Topic': str(item['Topic']).strip(),
                        'Question_Text': str(item.get('Question_Text', '')).strip(),
                        'Marks': int(item['Marks'])
                    }
                    for item in data
                    if all(k in item for k in ['Q_No', 'Topic', 'Marks'])
                ])
            else:
                st.error("Could not parse JSON from Groq response")
                return None
                
        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")
            return None


# ==================== DATABASE ====================

def save_test(data):
    data['id'] = len(st.session_state.tests_db) + 1
    data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.tests_db.append(data)

def reset_all():
    st.session_state.current_test = {
        'test_name': '',
        'class_section': '',
        'questions_df': pd.DataFrame(columns=['Q_No', 'Topic', 'Question_Text', 'Marks']),
        'extracted_text': ''
    }
    st.session_state.show_editor = False


# ==================== UI ====================

st.title("📚 Create Test")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📁 Saved Tests")
    if st.session_state.tests_db:
        for t in st.session_state.tests_db:
            with st.expander(f"📝 {t['test_name'][:20]}..."):
                st.write(f"Class: {t['class_section']}")
                st.write(f"Questions: {t['total_questions']}")
                st.write(f"Marks: {t['total_marks']}")
    else:
        st.info("No tests saved")

# Main
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("Test Details")
    test_name = st.text_input("Test Name *", placeholder="e.g., Chemistry Test 1")
    subject = st.text_input("Subject *", placeholder="e.g., Chemistry")
    class_section = st.selectbox(
        "Class & Section *",
        ["9-A", "9-B", "10-A", "10-B", "11-Science-A", "11-Commerce-A", "12-Science-A", "12-Commerce-A"]
    )

with c2:
    st.subheader("Upload Question Paper")
    uploaded = st.file_uploader("Choose PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    if uploaded:
        st.success(f"📎 {uploaded.name}")
        if uploaded.type.startswith('image'):
            st.image(uploaded, width=200)
        
        if st.button("🔍 Extract & Analyze", type="primary", use_container_width=True):
            file_bytes = uploaded.getvalue()
            
            with st.spinner("Extracting text..."):
                extracted = extract_text(file_bytes, uploaded.type)
            
            if extracted and len(extracted.strip()) > 50:
                st.session_state.current_test['extracted_text'] = extracted
                
                # Show extracted text
                st.markdown("---")
                st.subheader("📄 Extracted Text")
                st.text_area("Content:", extracted, height=250)
                
                # Analyze
                with st.spinner("Analyzing with AI..."):
                    analyzer = QuestionAnalyzer()
                    df = analyzer.analyze(extracted, class_section, subject)
                
                if df is not None and not df.empty:
                    st.session_state.current_test['questions_df'] = df
                    st.session_state.show_editor = True
                    st.rerun()
            else:
                st.error("Could not extract text. Try a clearer file.")

# Manual entry
st.markdown("---")
if st.button("✏️ Or Create Manually"):
    st.session_state.current_test['questions_df'] = pd.DataFrame([
        {'Q_No': 1, 'Topic': '', 'Question_Text': '', 'Marks': 0}
    ])
    st.session_state.show_editor = True
    st.rerun()

# Editor
if st.session_state.show_editor:
    st.markdown("---")
    st.subheader("📝 Questions")
    
    df = st.session_state.current_test['questions_df'].copy()
    if not df.empty:
        df['Q_No'] = df['Q_No'].astype(int)
        df['Marks'] = df['Marks'].astype(int)
    
    edited = st.data_editor(
        df,
        column_config={
            "Q_No": st.column_config.NumberColumn("Q.No", min_value=1, step=1, required=True),
            "Topic": st.column_config.TextColumn("Topic", required=True),
            "Question_Text": st.column_config.TextColumn("Question", width="large"),
            "Marks": st.column_config.NumberColumn("Marks", min_value=0, step=1, required=True)
        },
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="editor"
    )
    
    st.session_state.current_test['questions_df'] = edited
    
    # Summary & Save
    st.markdown("---")
    cols = st.columns(4)
    cols[0].metric("Questions", len(edited))
    cols[1].metric("Total Marks", int(edited['Marks'].sum()) if not edited.empty else 0)
    cols[2].metric("Topics", edited['Topic'].nunique() if not edited.empty else 0)
    
    if not edited.empty and 'Topic' in edited.columns:
        st.bar_chart(edited.groupby('Topic')['Marks'].sum())
    
    st.markdown("---")
    sc = st.columns([1, 1, 2])
    
    if sc[0].button("❌ Cancel"):
        reset_all()
        st.rerun()
    
    if sc[1].button("💾 Save Test", type="primary"):
        if not test_name.strip():
            st.error("Enter test name!")
        elif edited.empty or edited['Topic'].isna().any() or (edited['Topic'] == '').any():
            st.error("Fill all topics!")
        elif edited['Marks'].isna().any():
            st.error("Fill all marks!")
        else:
            save_test({
                'test_name': test_name.strip(),
                'class_section': class_section,
                'questions': edited.to_dict('records'),
                'total_questions': len(edited),
                'total_marks': int(edited['Marks'].sum()),
                'topics': edited['Topic'].unique().tolist()
            })
            st.success("✅ Test saved!")
            st.balloons()
            reset_all()
            st.rerun()