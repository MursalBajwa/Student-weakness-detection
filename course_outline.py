import streamlit as st
import pandas as pd

st.set_page_config(page_title="Course Outline Manager", page_icon="📚", layout="wide")

# ============================================================
# SESSION STATE - Course Outlines Database
# ============================================================

if 'course_outlines_db' not in st.session_state:
    # Initial course outlines (same as your existing data)
    st.session_state.course_outlines_db = {
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
        11: {
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
        12: {
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

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_subjects_for_class(class_num):
    """Get all subjects for a given class number"""
    return list(st.session_state.course_outlines_db.get(class_num, {}).keys())

def get_outline(class_num, subject):
    """Get topics for a class and subject"""
    return st.session_state.course_outlines_db.get(class_num, {}).get(subject.lower(), [])

def save_outline(class_num, subject, topics):
    """Save updated topics for a class and subject"""
    if class_num not in st.session_state.course_outlines_db:
        st.session_state.course_outlines_db[class_num] = {}
    st.session_state.course_outlines_db[class_num][subject.lower()] = topics

def delete_subject(class_num, subject):
    """Delete a subject from a class"""
    if class_num in st.session_state.course_outlines_db:
        if subject.lower() in st.session_state.course_outlines_db[class_num]:
            del st.session_state.course_outlines_db[class_num][subject.lower()]

def delete_class(class_num):
    """Delete an entire class"""
    if class_num in st.session_state.course_outlines_db:
        del st.session_state.course_outlines_db[class_num]

# ============================================================
# UI
# ============================================================

st.title("📚 Course Outline Manager")
st.markdown("Manage subject topics for each class. Add, edit, or delete topics easily.")
st.markdown("---")

# ── Sidebar: Overview ──
with st.sidebar:
    st.header("📊 Overview")
    total_classes = len(st.session_state.course_outlines_db)
    total_subjects = sum(len(subjects) for subjects in st.session_state.course_outlines_db.values())
    total_topics = sum(
        len(topics) 
        for subjects in st.session_state.course_outlines_db.values() 
        for topics in subjects.values()
    )

    st.metric("Total Classes", total_classes)
    st.metric("Total Subjects", total_subjects)
    st.metric("Total Topics", total_topics)

    st.markdown("---")
    st.caption("Student Weakness Detection System")

# ── Main: Two Columns ──
left_col, right_col = st.columns([1, 2])

# ── LEFT COLUMN: Selection ──
with left_col:
    st.subheader("1️⃣ Select Class & Subject")

    # Class selection
    all_classes = sorted(st.session_state.course_outlines_db.keys())
    selected_class = st.selectbox(
        "Select Class",
        options=["-- Select Class --"] + all_classes,
        format_func=lambda x: f"Class {x}" if isinstance(x, int) else x,
        index=0
    )

    if selected_class == "-- Select Class --":
        st.info("👆 Select a class to continue")
        st.stop()

    # Subject selection
    subjects = get_subjects_for_class(selected_class)
    subject_display = [s.title().replace("_", " ") for s in subjects]
    subject_key_map = {s.title().replace("_", " "): s for s in subjects}

    selected_subject_display = st.selectbox(
        "Select Subject",
        options=["-- Select Subject --"] + subject_display,
        index=0
    )

    if selected_subject_display == "-- Select Subject --":
        st.info("👆 Select a subject to view/edit topics")
        st.stop()

    selected_subject = subject_key_map[selected_subject_display]
    current_topics = get_outline(selected_class, selected_subject)

    # Show current topics count
    st.caption(f"📋 {len(current_topics)} topics in this outline")

# ── RIGHT COLUMN: Topic Editor ──
with right_col:
    st.subheader(f"2️⃣ Manage Topics — Class {selected_class} | {selected_subject_display}")

    # Convert topics to DataFrame for editing
    if current_topics:
        df_topics = pd.DataFrame({
            "S.No": range(1, len(current_topics) + 1),
            "Topic": current_topics
        })
    else:
        df_topics = pd.DataFrame({"S.No": [1], "Topic": [""]})

    # Data editor for topics
    edited_df = st.data_editor(
        df_topics,
        column_config={
            "S.No": st.column_config.NumberColumn("S.No", disabled=True),
            "Topic": st.column_config.TextColumn("Topic Name", required=True, width="large")
        },
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="topic_editor"
    )

    # Remove empty rows
    edited_df = edited_df[edited_df["Topic"].str.strip() != ""].reset_index(drop=True)
    edited_df["S.No"] = range(1, len(edited_df) + 1)

    st.markdown("---")

    # Action buttons
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])

    with btn_col1:
        if st.button("💾 Save Changes", type="primary", use_container_width=True):
            topics_list = edited_df["Topic"].str.strip().tolist()
            if not topics_list:
                st.error("❌ Cannot save empty outline. Add at least one topic.")
            else:
                save_outline(selected_class, selected_subject, topics_list)
                st.success(f"✅ Saved {len(topics_list)} topics for Class {selected_class} - {selected_subject_display}")
                st.rerun()

    with btn_col2:
        if st.button("🗑️ Delete Subject", use_container_width=True):
            delete_subject(selected_class, selected_subject)
            st.success(f"🗑️ Deleted {selected_subject_display} from Class {selected_class}")
            st.rerun()

    with btn_col3:
        if st.button("➕ Add New Subject", use_container_width=True):
            st.session_state.show_add_subject = True
            st.rerun()

# ── ADD NEW SUBJECT SECTION ──
if st.session_state.get("show_add_subject", False):
    st.markdown("---")
    st.subheader("➕ Add New Subject")

    add_col1, add_col2 = st.columns([1, 2])

    with add_col1:
        new_subject_name = st.text_input(
            "Subject Name",
            placeholder="e.g., Computer Science",
            key="new_subject_name"
        )

        new_class = st.selectbox(
            "For Class",
            options=sorted(st.session_state.course_outlines_db.keys()),
            format_func=lambda x: f"Class {x}",
            key="new_subject_class"
        )

    with add_col2:
        new_topics_text = st.text_area(
            "Topics (one per line)",
            placeholder="Enter topics, one per line...\n\nExample:\nIntroduction to Subject\nBasic Concepts\nAdvanced Topics",
            height=200,
            key="new_topics_text"
        )

    save_col1, save_col2 = st.columns([1, 3])

    with save_col1:
        if st.button("✅ Create Subject", type="primary", use_container_width=True):
            if not new_subject_name.strip():
                st.error("❌ Subject name cannot be empty")
            elif not new_topics_text.strip():
                st.error("❌ Please enter at least one topic")
            else:
                topics = [t.strip() for t in new_topics_text.split("\n") if t.strip()]
                save_outline(new_class, new_subject_name.strip(), topics)
                st.session_state.show_add_subject = False
                st.success(f"✅ Created '{new_subject_name.strip()}' with {len(topics)} topics for Class {new_class}")
                st.rerun()

    with save_col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_add_subject = False
            st.rerun()

# ── VIEW ALL OUTLINES ──
st.markdown("---")
st.subheader("📋 All Course Outlines")

for class_num in sorted(st.session_state.course_outlines_db.keys()):
    subjects = st.session_state.course_outlines_db[class_num]
    with st.expander(f"🎓 Class {class_num} ({len(subjects)} subjects, {sum(len(t) for t in subjects.values())} topics)"):
        for subject, topics in subjects.items():
            subject_display = subject.title().replace("_", " ")
            st.markdown(f"**📖 {subject_display}** — {len(topics)} topics")
            for i, topic in enumerate(topics, 1):
                st.write(f"   {i}. {topic}")
            st.markdown("---")

# ── DELETE CLASS SECTION ──
st.markdown("---")
st.subheader("⚠️ Danger Zone")

del_col1, del_col2 = st.columns([1, 3])
with del_col1:
    class_to_delete = st.selectbox(
        "Select Class to Delete",
        options=["-- Select --"] + sorted(st.session_state.course_outlines_db.keys()),
        format_func=lambda x: f"Class {x}" if isinstance(x, int) else x,
        key="class_to_delete"
    )

with del_col2:
    if class_to_delete != "-- Select --":
        if st.button(f"🗑️ Delete Entire Class {class_to_delete}", type="secondary", use_container_width=True):
            delete_class(class_to_delete)
            st.success(f"🗑️ Deleted Class {class_to_delete} and all its subjects")
            st.rerun()