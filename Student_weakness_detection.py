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
from langchain_ollama import OllamaLLM

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
        'questions_df': pd.DataFrame(columns=['Q_No', 'Topic', 'Question_Text', 'Marks', 'Question_Type']),
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
        self.llm = OllamaLLM(model="llama3.2:3b", temperature=0.1)

    def analyze(self, text_content, class_section, subject):
        # Get the course outline topics
        outline_topics = get_outline(class_section, subject)

        if not outline_topics:
            st.warning(f"No course outline found for Class {class_section} - Subject: {subject}. Using auto-detection.")
            outline_topics_str = "Detect topic from question content"
        else:
            outline_topics_str = "\n".join([f"  - {t}" for t in outline_topics])

        prompt = f"""You are an expert educational content analyzer. Your task is to extract ALL questions from the given exam paper text.

CLASS INFORMATION:
- Class: {class_section}
- Subject: {subject}

ALLOWED TOPICS (MUST choose from this list only):
{outline_topics_str}

EXTRACTION RULES - FOLLOW STRICTLY:
1. Extract EVERY SINGLE question found in the text - do NOT skip any question
2. For each question, identify:
   - Q_No: The question number as shown in the paper (1, 2, 3, etc.)
   - Topic: MUST be one of the allowed topics listed above. Choose the closest match based on question content.
   - Question_Text: The FULL question text (keep it concise but complete, max 200 characters)
   - Marks: The marks assigned to this question. If not explicitly stated, use these defaults:
     * MCQ questions: 1 mark each
     * Short questions: 2 marks each  
     * Long/Detailed questions: 5 marks each
   - Question_Type: One of: "MCQ", "Short", "Long"

3. QUESTION TYPE DETECTION:
   - "MCQ": Questions with options like (a), (b), (c), (d) or multiple choice format
   - "Short": Questions asking for brief answers, definitions, short explanations (1-3 lines expected)
   - "Long": Questions asking for detailed answers, descriptions, explanations, essays

4. IMPORTANT:
   - Do NOT miss any question - scan the entire text carefully
   - If a question has sub-parts (a, b, c), treat each sub-part as a separate question with its own Q_No
   - Ignore headers, footers, instructions like "Tick the correct option", "Answer any 8", etc.
   - Ignore bubble sheets, logos, website URLs, student info fields
   - IGNORE SECTION LABELS: Text like "Section A", "Section B", "Part I", "Part II", "Unit#1", "Test#1", "Q.1", "Q.2" (when used as section headers), "Short Questions", "Long Questions", "MCQs" — these are NOT questions, do NOT include them
   - Only extract actual questions that students need to answer
   - If marks are written next to questions (like "[5]" or "(3 marks)"), extract that number
   - If no marks are shown, use the default values based on question type

5. OUTPUT FORMAT:
   Return ONLY a valid JSON array. No explanations, no markdown code blocks, just pure JSON.
   Example format:
   [
     {{"Q_No": 1, "Topic": "Chemical Equilibrium", "Question_Text": "The unit of molar concentration is", "Marks": 1, "Question_Type": "MCQ"}},
     {{"Q_No": 2, "Topic": "Chemical Equilibrium", "Question_Text": "What do you mean by equilibrium constant?", "Marks": 2, "Question_Type": "Short"}}
   ]

EXAM PAPER TEXT TO ANALYZE:
{text_content[:7000]}

JSON OUTPUT:"""

        try:
            response = self.llm.invoke(prompt)

            # Try multiple patterns to extract JSON
            json_data = None

            # Pattern 1: Look for JSON array between brackets
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                try:
                    json_data = json.loads(match.group())
                except:
                    pass

            # Pattern 2: Look for JSON array with code block
            if not json_data:
                match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response, re.DOTALL)
                if match:
                    try:
                        json_data = json.loads(match.group(1))
                    except:
                        pass

            # Pattern 3: Try to find any JSON-like structure
            if not json_data:
                # Try to clean the response and parse
                cleaned = response.strip()
                if cleaned.startswith('[') and cleaned.endswith(']'):
                    try:
                        json_data = json.loads(cleaned)
                    except:
                        pass

            if json_data:
                # Validate and clean the data
                validated_data = []
                for item in json_data:
                    if isinstance(item, dict):
                        # Ensure all required fields exist
                        q_no = item.get('Q_No', item.get('q_no', item.get('question_no', 0)))
                        topic_val = item.get('Topic', item.get('topic', 'Unknown'))
                        question_text = item.get('Question_Text', item.get('question_text', item.get('text', '')))
                        marks = item.get('Marks', item.get('marks', item.get('mark', 1)))
                        q_type = item.get('Question_Type', item.get('question_type', item.get('type', 'Short')))

                        # Validate topic against outline
                        if outline_topics and topic_val not in outline_topics:
                            # Find closest match
                            topic_val = self._find_closest_topic(topic_val, outline_topics)

                        validated_data.append({
                            'Q_No': int(q_no) if q_no else 0,
                            'Topic': str(topic_val).strip(),
                            'Question_Text': str(question_text).strip(),
                            'Marks': int(marks) if marks else 1,
                            'Question_Type': str(q_type).strip()
                        })

                if validated_data:
                    return pd.DataFrame(validated_data)

            st.warning("Could not parse LLM response into valid question data. Please try manual entry.")
            return None

        except Exception as e:
            st.error(f"LLM Error: {str(e)}")
            return None

    def _find_closest_topic(self, detected_topic, allowed_topics):
        """Find the closest matching topic from allowed list"""
        detected_lower = detected_topic.lower()

        # Direct match
        for topic in allowed_topics:
            if topic.lower() == detected_lower:
                return topic

        # Partial match
        for topic in allowed_topics:
            if detected_lower in topic.lower() or topic.lower() in detected_lower:
                return topic

        # Return first topic as fallback (or could use more sophisticated matching)
        return allowed_topics[0] if allowed_topics else detected_topic


# ==================== DATABASE ====================

def save_test(data):
    data['id'] = len(st.session_state.tests_db) + 1
    data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.tests_db.append(data)

def reset_all():
    st.session_state.current_test = {
        'test_name': '',
        'class_section': '',
        'questions_df': pd.DataFrame(columns=['Q_No', 'Topic', 'Question_Text', 'Marks', 'Question_Type']),
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

    # Show available topics for selected class and subject
    if subject:
        available_topics = get_outline(class_section, subject)
        if available_topics:
            with st.expander("📋 Available Topics"):
                for t in available_topics:
                    st.write(f"• {t}")

with c2:
    st.subheader("Upload Question Paper")
    uploaded = st.file_uploader("Choose PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])

    if uploaded:
        st.success(f"📎 {uploaded.name}")
        if uploaded.type.startswith('image'):
            st.image(uploaded, width=200)

        if st.button("🔍 Extract & Analyze", type="primary", use_container_width=True):
            if not subject.strip():
                st.error("Please enter Subject first!")
            else:
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
        {'Q_No': 1, 'Topic': '', 'Question_Text': '', 'Marks': 0, 'Question_Type': 'Short'}
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

    # Get available topics for dropdown
    available_topics = get_outline(class_section, subject) if subject else []

    edited = st.data_editor(
        df,
        column_config={
            "Q_No": st.column_config.NumberColumn("Q.No", min_value=1, step=1, required=True),
            "Topic": st.column_config.SelectboxColumn(
                "Topic", 
                options=available_topics if available_topics else ["Enter subject first"],
                required=True
            ),
            "Question_Text": st.column_config.TextColumn("Question", width="large"),
            "Marks": st.column_config.NumberColumn("Marks", min_value=0, step=1, required=True),
            "Question_Type": st.column_config.SelectboxColumn(
                "Type",
                options=["MCQ", "Short", "Long"],
                required=True
            )
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