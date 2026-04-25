import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Student Marking", page_icon="✅", layout="wide")

# ==================== STATIC DATA ====================

# Students organized by class-section
STUDENTS_DB = {
    "9-A": [
        {"id": 1, "name": "Ahmed Khan", "roll_no": "101"},
        {"id": 2, "name": "Fatima Ali", "roll_no": "102"},
        {"id": 3, "name": "Usman Raza", "roll_no": "103"},
        {"id": 4, "name": "Ayesha Noor", "roll_no": "104"},
        {"id": 5, "name": "Bilal Ahmad", "roll_no": "105"},
        {"id": 6, "name": "Zara Hussain", "roll_no": "106"},
    ],
    "9-B": [
        {"id": 7, "name": "Hassan Javed", "roll_no": "201"},
        {"id": 8, "name": "Maryam Tariq", "roll_no": "202"},
        {"id": 9, "name": "Omar Farooq", "roll_no": "203"},
        {"id": 10, "name": "Sana Iqbal", "roll_no": "204"},
        {"id": 11, "name": "Imran Sheikh", "roll_no": "205"},
    ],
    "10-A": [
        {"id": 12, "name": "Ali Raza", "roll_no": "301"},
        {"id": 13, "name": "Hira Khan", "roll_no": "302"},
        {"id": 14, "name": "Saad Malik", "roll_no": "303"},
        {"id": 15, "name": "Nida Fatima", "roll_no": "304"},
        {"id": 16, "name": "Waqar Ahmed", "roll_no": "305"},
        {"id": 17, "name": "Rabia Sultana", "roll_no": "306"},
        {"id": 18, "name": "Tariq Mehmood", "roll_no": "307"},
    ],
    "10-B": [
        {"id": 19, "name": "Kamran Ali", "roll_no": "401"},
        {"id": 20, "name": "Sadia Bibi", "roll_no": "402"},
        {"id": 21, "name": "Noman Haider", "roll_no": "403"},
        {"id": 22, "name": "Fiza Khan", "roll_no": "404"},
        {"id": 23, "name": "Shahid Afridi", "roll_no": "405"},
    ],
    "11-Science-A": [
        {"id": 24, "name": "Danish Tariq", "roll_no": "501"},
        {"id": 25, "name": "Amina Zahra", "roll_no": "502"},
        {"id": 26, "name": "Fahad Mustafa", "roll_no": "503"},
        {"id": 27, "name": "Laiba Noor", "roll_no": "504"},
        {"id": 28, "name": "Zain Abbas", "roll_no": "505"},
        {"id": 29, "name": "Mehwish Hayat", "roll_no": "506"},
    ],
    "11-Commerce-A": [
        {"id": 30, "name": "Asif Ali", "roll_no": "601"},
        {"id": 31, "name": "Nimra Khan", "roll_no": "602"},
        {"id": 32, "name": "Rizwan Ahmed", "roll_no": "603"},
        {"id": 33, "name": "Saba Qamar", "roll_no": "604"},
    ],
    "12-Science-A": [
        {"id": 34, "name": "Hamza Ali", "roll_no": "701"},
        {"id": 35, "name": "Iqra Aziz", "roll_no": "702"},
        {"id": 36, "name": "Babar Azam", "roll_no": "703"},
        {"id": 37, "name": "Maya Ali", "roll_no": "704"},
        {"id": 38, "name": "Shaheen Afridi", "roll_no": "705"},
        {"id": 39, "name": "Mahira Khan", "roll_no": "706"},
    ],
    "12-Commerce-A": [
        {"id": 40, "name": "Shoaib Akhtar", "roll_no": "801"},
        {"id": 41, "name": "Hania Amir", "roll_no": "802"},
        {"id": 42, "name": "Wasim Akram", "roll_no": "803"},
        {"id": 43, "name": "Sajal Aly", "roll_no": "804"},
    ],
}

# Static Tests Database
TESTS_DB = [
    {
        "id": 1,
        "test_name": "Chemistry Unit Test 1",
        "class_section": "10-A",
        "subject": "Chemistry",
        "total_questions": 16,
        "total_marks": 30,
        "questions": [
            {"Q_No": 1, "Topic": "Chemical Equilibrium", "Question_Text": "The unit of molar concentration is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 2, "Topic": "Chemical Equilibrium", "Question_Text": "Unit of active mass is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 3, "Topic": "Chemical Equilibrium", "Question_Text": "Who proposed law of mass action", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 4, "Topic": "Chemical Equilibrium", "Question_Text": "The color of HI is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 5, "Topic": "Chemical Equilibrium", "Question_Text": "Kc is always equal to", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 6, "Topic": "Chemical Equilibrium", "Question_Text": "What do you mean by equilibrium constant", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 7, "Topic": "Chemical Equilibrium", "Question_Text": "What is active mass", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 8, "Topic": "Chemical Equilibrium", "Question_Text": "Define law of mass action", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 9, "Topic": "Chemical Equilibrium", "Question_Text": "Define reversible reactions", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 10, "Topic": "Chemical Equilibrium", "Question_Text": "Give two properties of reverse reaction", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 11, "Topic": "Chemical Equilibrium", "Question_Text": "What is extent of reaction", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 12, "Topic": "Chemical Equilibrium", "Question_Text": "Define static equilibrium with example", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 13, "Topic": "Chemical Equilibrium", "Question_Text": "What is relation between active mass and rate of reaction", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 14, "Topic": "Chemical Equilibrium", "Question_Text": "What is chemical equilibrium state", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 15, "Topic": "Chemical Equilibrium", "Question_Text": "Describe importance of equilibrium", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 16, "Topic": "Chemical Equilibrium", "Question_Text": "State law of mass action", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 2,
        "test_name": "Physics Mid-Term Exam",
        "class_section": "10-A",
        "subject": "Physics",
        "total_questions": 12,
        "total_marks": 50,
        "questions": [
            {"Q_No": 1, "Topic": "Simple Harmonic Motion and Waves", "Question_Text": "Define simple harmonic motion", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 2, "Topic": "Simple Harmonic Motion and Waves", "Question_Text": "What is time period of a pendulum", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Sound", "Question_Text": "Speed of sound in air at 0°C is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 4, "Topic": "Sound", "Question_Text": "What is echo", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 5, "Topic": "Geometrical Optics", "Question_Text": "Law of reflection states that", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 6, "Topic": "Geometrical Optics", "Question_Text": "Define focal length of a mirror", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 7, "Topic": "Electrostatics", "Question_Text": "Unit of electric charge is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 8, "Topic": "Electrostatics", "Question_Text": "State Coulomb's law", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 9, "Topic": "Current Electricity", "Question_Text": "Ohm's law formula is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 10, "Topic": "Current Electricity", "Question_Text": "Define electrical resistance", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 11, "Topic": "Simple Harmonic Motion and Waves", "Question_Text": "Derive the equation for velocity of wave", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 12, "Topic": "Electrostatics", "Question_Text": "Explain electric field and electric potential in detail", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 3,
        "test_name": "Biology Chapter Test",
        "class_section": "10-B",
        "subject": "Biology",
        "total_questions": 10,
        "total_marks": 25,
        "questions": [
            {"Q_No": 1, "Topic": "Gaseous Exchange", "Question_Text": "Site of gaseous exchange in humans is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 2, "Topic": "Gaseous Exchange", "Question_Text": "What is breathing rate", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Homeostasis", "Question_Text": "Define homeostasis", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 4, "Topic": "Homeostasis", "Question_Text": "Name the organ responsible for osmoregulation", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 5, "Topic": "Coordination and Control", "Question_Text": "What is a reflex action", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 6, "Topic": "Coordination and Control", "Question_Text": "Part of brain controlling balance is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 7, "Topic": "Support and Movement", "Question_Text": "Types of joints in human body", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 8, "Topic": "Reproduction", "Question_Text": "Define asexual reproduction", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 9, "Topic": "Gaseous Exchange", "Question_Text": "Describe the mechanism of breathing in humans", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 10, "Topic": "Homeostasis", "Question_Text": "Explain the role of kidney in maintaining homeostasis", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 4,
        "test_name": "Math Quiz 1",
        "class_section": "9-A",
        "subject": "Mathematics",
        "total_questions": 8,
        "total_marks": 20,
        "questions": [
            {"Q_No": 1, "Topic": "Real Numbers", "Question_Text": "Value of pi is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 2, "Topic": "Real Numbers", "Question_Text": "Define rational number", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Logarithms", "Question_Text": "Log(1) equals to", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 4, "Topic": "Logarithms", "Question_Text": "State product rule of logarithms", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 5, "Topic": "Sets and Functions", "Question_Text": "Define union of two sets", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 6, "Topic": "Sets and Functions", "Question_Text": "What is a function", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 7, "Topic": "Real Numbers", "Question_Text": "Prove that sqrt(2) is irrational", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 8, "Topic": "Logarithms", "Question_Text": "Solve: log(x) + log(2) = log(10)", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 5,
        "test_name": "Chemistry Equilibrium Test",
        "class_section": "11-Science-A",
        "subject": "Chemistry",
        "total_questions": 10,
        "total_marks": 40,
        "questions": [
            {"Q_No": 1, "Topic": "Chemical Equilibrium", "Question_Text": "State Le Chatelier's principle", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 2, "Topic": "Chemical Equilibrium", "Question_Text": "What is equilibrium constant Kp", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Reaction Kinetics", "Question_Text": "Define rate of reaction", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 4, "Topic": "Reaction Kinetics", "Question_Text": "Unit of rate constant for first order reaction", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 5, "Topic": "Chemical Energetics", "Question_Text": "Enthalpy change is denoted by", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 6, "Topic": "Chemical Energetics", "Question_Text": "Define exothermic reaction", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 7, "Topic": "States of Matter", "Question_Text": "Boyle's law states that", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 8, "Topic": "States of Matter", "Question_Text": "What is ideal gas equation", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 9, "Topic": "Chemical Equilibrium", "Question_Text": "Derive the relation between Kp and Kc", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 10, "Topic": "Reaction Kinetics", "Question_Text": "Explain collision theory of reaction rates", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 6,
        "test_name": "Physics Measurements Quiz",
        "class_section": "11-Science-A",
        "subject": "Physics",
        "total_questions": 8,
        "total_marks": 25,
        "questions": [
            {"Q_No": 1, "Topic": "Measurements", "Question_Text": "SI unit of length is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 2, "Topic": "Measurements", "Question_Text": "Define significant figures", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Vectors and Equilibrium", "Question_Text": "What is a vector quantity", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 4, "Topic": "Vectors and Equilibrium", "Question_Text": "State conditions for equilibrium", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 5, "Topic": "Motion and Force", "Question_Text": "Newton's second law formula", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 6, "Topic": "Motion and Force", "Question_Text": "Define momentum", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 7, "Topic": "Measurements", "Question_Text": "Explain the use of vernier caliper with diagram", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 8, "Topic": "Vectors and Equilibrium", "Question_Text": "Derive the rectangular components of a vector", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 7,
        "test_name": "Computer Science Fundamentals",
        "class_section": "11-Commerce-A",
        "subject": "Computer Science",
        "total_questions": 8,
        "total_marks": 30,
        "questions": [
            {"Q_No": 1, "Topic": "Introduction to IT", "Question_Text": "Full form of CPU is", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 2, "Topic": "Introduction to IT", "Question_Text": "What is information technology", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Data Representation", "Question_Text": "Convert binary 1010 to decimal", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 4, "Topic": "Data Representation", "Question_Text": "What is ASCII code", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 5, "Topic": "Computer Architecture", "Question_Text": "Name the components of CPU", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 6, "Topic": "Operating Systems", "Question_Text": "Functions of operating system", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 7, "Topic": "Programming Fundamentals", "Question_Text": "What is an algorithm", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 8, "Topic": "Programming Fundamentals", "Question_Text": "Write an algorithm to find factorial of a number", "Marks": 5, "Question_Type": "Long"},
        ]
    },
    {
        "id": 8,
        "test_name": "Biology 12 - Final Prep",
        "class_section": "12-Science-A",
        "subject": "Biology",
        "total_questions": 10,
        "total_marks": 45,
        "questions": [
            {"Q_No": 1, "Topic": "Homeostasis", "Question_Text": "Define feedback mechanism", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 2, "Topic": "Support and Movement", "Question_Text": "Types of muscles in human body", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 3, "Topic": "Coordination and Control", "Question_Text": "What is a synapse", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 4, "Topic": "Reproduction", "Question_Text": "Define parthenogenesis", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 5, "Topic": "Growth and Development", "Question_Text": "What is metamorphosis", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 6, "Topic": "Chromosomes and DNA", "Question_Text": "Structure of DNA was discovered by", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 7, "Topic": "Chromosomes and DNA", "Question_Text": "Explain DNA replication process", "Marks": 5, "Question_Type": "Long"},
            {"Q_No": 8, "Topic": "Biotechnology", "Question_Text": "What is genetic engineering", "Marks": 2, "Question_Type": "Short"},
            {"Q_No": 9, "Topic": "Evolution", "Question_Text": "Theory of natural selection was given by", "Marks": 1, "Question_Type": "MCQ"},
            {"Q_No": 10, "Topic": "Ecosystem", "Question_Text": "Describe the components of an ecosystem", "Marks": 5, "Question_Type": "Long"},
        ]
    },
]

# ==================== SESSION STATE ====================

if 'marks_db' not in st.session_state:
    st.session_state.marks_db = []  # Stores: {test_id, student_id, student_name, class_section, marks_data, total_gained, date}

if 'selected_test' not in st.session_state:
    st.session_state.selected_test = None

if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None

if 'marking_df' not in st.session_state:
    st.session_state.marking_df = None

if 'show_marking_form' not in st.session_state:
    st.session_state.show_marking_form = False

def reset_marking():
    st.session_state.selected_test = None
    st.session_state.selected_student = None
    st.session_state.marking_df = None
    st.session_state.show_marking_form = False

# ==================== SIDEBAR ====================

with st.sidebar:
    st.title("🎓 Marking Portal")
    st.markdown("---")

    st.header("📊 Saved Marks Records")
    if st.session_state.marks_db:
        for record in st.session_state.marks_db:
            with st.expander(f"📝 {record['student_name']} - {record['test_name'][:20]}..."):
                st.write(f"Class: {record['class_section']}")
                st.write(f"Test: {record['test_name']}")
                st.write(f"Gained: {record['total_gained']} / {record['total_marks']}")
                st.write(f"Date: {record['date']}")
    else:
        st.info("No marks recorded yet")

    st.markdown("---")
    st.caption("Student Weakness Detection System")

# ==================== MAIN UI ====================

st.title("✅ Student Marking")
st.markdown("---")

# Step 1: Select Test
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1️⃣ Select Test")
    test_options = {f"{t['test_name']} ({t['class_section']})": t for t in TESTS_DB}
    selected_test_label = st.selectbox(
        "Choose a test",
        options=["-- Select Test --"] + list(test_options.keys()),
        index=0
    )

    if selected_test_label != "-- Select Test --":
        st.session_state.selected_test = test_options[selected_test_label]
        test = st.session_state.selected_test

        # Show test info
        info_col1, info_col2, info_col3 = st.columns(3)
        info_col1.metric("Class", test['class_section'])
        info_col2.metric("Subject", test['subject'])
        info_col3.metric("Total Marks", test['total_marks'])

        with st.expander("📋 View Test Questions"):
            for q in test['questions']:
                st.write(f"**Q{q['Q_No']}.** {q['Question_Text']} ({q['Question_Type']}) — *{q['Marks']} marks*")

with col2:
    st.subheader("2️⃣ Select Student")

    if st.session_state.selected_test is None:
        st.info("👈 Please select a test first")
    else:
        test = st.session_state.selected_test
        class_section = test['class_section']
        students = STUDENTS_DB.get(class_section, [])

        if not students:
            st.warning(f"No students found for {class_section}")
        else:
            student_options = {f"{s['roll_no']} - {s['name']}": s for s in students}
            selected_student_label = st.selectbox(
                f"Choose student from {class_section}",
                options=["-- Select Student --"] + list(student_options.keys()),
                index=0
            )

            if selected_student_label != "-- Select Student --":
                st.session_state.selected_student = student_options[selected_student_label]
                student = st.session_state.selected_student

                st.success(f"Selected: **{student['name']}** (Roll: {student['roll_no']})")

                # Check if already marked
                existing = [r for r in st.session_state.marks_db 
                           if r['test_id'] == test['id'] and r['student_id'] == student['id']]
                if existing:
                    st.warning(f"⚠️ Already marked! Gained: {existing[0]['total_gained']}/{existing[0]['total_marks']}")

# Step 3: Marking Form
st.markdown("---")

if st.session_state.selected_test and st.session_state.selected_student:
    st.subheader("3️⃣ Enter Marks")

    test = st.session_state.selected_test
    student = st.session_state.selected_student

    # Prepare marking dataframe
    if st.session_state.marking_df is None:
        df_data = []
        for q in test['questions']:
            df_data.append({
                'Q_No': q['Q_No'],
                'Topic': q['Topic'],
                'Question': q['Question_Text'],
                'Type': q['Question_Type'],
                'Total_Marks': q['Marks'],
                'Gained_Marks': 0
            })
        st.session_state.marking_df = pd.DataFrame(df_data)

    # Show marking editor
    edited_df = st.data_editor(
        st.session_state.marking_df,
        column_config={
            "Q_No": st.column_config.NumberColumn("Q.No", disabled=True),
            "Topic": st.column_config.TextColumn("Topic", disabled=True),
            "Question": st.column_config.TextColumn("Question", width="large", disabled=True),
            "Type": st.column_config.TextColumn("Type", disabled=True),
            "Total_Marks": st.column_config.NumberColumn("Total", disabled=True),
            "Gained_Marks": st.column_config.NumberColumn(
                "Gained",
                min_value=0,
                step=1,
                required=True,
                help="Enter marks obtained by student"
            )
        },
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        key="marking_editor"
    )

    st.session_state.marking_df = edited_df

    # Summary
    total_gained = int(edited_df['Gained_Marks'].sum()) if not edited_df.empty else 0
    total_marks = test['total_marks']
    percentage = round((total_gained / total_marks) * 100, 1) if total_marks > 0 else 0

    st.markdown("---")
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    sum_col1.metric("Total Questions", len(edited_df))
    sum_col2.metric("Gained Marks", total_gained)
    sum_col3.metric("Total Marks", total_marks)
    sum_col4.metric("Percentage", f"{percentage}%")

    # Topic-wise breakdown
    st.markdown("---")
    st.subheader("📊 Topic-wise Performance")
    topic_df = edited_df.groupby('Topic').agg({
        'Total_Marks': 'sum',
        'Gained_Marks': 'sum'
    }).reset_index()
    topic_df['Percentage'] = round((topic_df['Gained_Marks'] / topic_df['Total_Marks']) * 100, 1)

    st.dataframe(topic_df, use_container_width=True, hide_index=True)

    # Bar chart
    st.bar_chart(topic_df.set_index('Topic')[['Gained_Marks', 'Total_Marks']])

    # Action buttons
    st.markdown("---")
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])

    with btn_col1:
        if st.button("❌ Cancel", use_container_width=True):
            reset_marking()
            st.rerun()

    with btn_col2:
        if st.button("💾 Save Marks", type="primary", use_container_width=True):
            # Validate
            invalid = edited_df[edited_df['Gained_Marks'] > edited_df['Total_Marks']]
            if not invalid.empty:
                st.error("❌ Gained marks cannot exceed total marks! Check Q.No: " + ", ".join(invalid['Q_No'].astype(str).tolist()))
            else:
                # Save record
                record = {
                    'id': len(st.session_state.marks_db) + 1,
                    'test_id': test['id'],
                    'test_name': test['test_name'],
                    'student_id': student['id'],
                    'student_name': student['name'],
                    'student_roll': student['roll_no'],
                    'class_section': test['class_section'],
                    'subject': test['subject'],
                    'marks_data': edited_df.to_dict('records'),
                    'total_gained': total_gained,
                    'total_marks': total_marks,
                    'percentage': percentage,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Remove existing record if present
                st.session_state.marks_db = [
                    r for r in st.session_state.marks_db 
                    if not (r['test_id'] == test['id'] and r['student_id'] == student['id'])
                ]
                st.session_state.marks_db.append(record)

                st.success(f"✅ Marks saved for {student['name']}! Total: {total_gained}/{total_marks} ({percentage}%)")
                st.balloons()
                reset_marking()
                st.rerun()

else:
    st.info("👆 Please select a test and student to start marking")