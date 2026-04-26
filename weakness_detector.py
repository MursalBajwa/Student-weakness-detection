import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Topic Weakness Detector", page_icon="🎯", layout="wide")

# ============================================================
# STATIC DATA
# ============================================================

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

# Course outlines by class and subject
COURSE_OUTLINE = {
    9: {
        "physics": ["Physical Quantities and Measurements", "Kinematics", "Dynamics", "Turning Effect of Forces", "Work, Energy and Power", "Gravitation", "Properties of Matter", "Thermal Properties of Matter", "Magnetism", "Nature of Science"],
        "chemistry": ["Introduction to Chemistry", "Structure of Atom", "Periodic Table and Periodicity", "Structure of Molecules", "Physical States of Matter", "Solutions", "Electrochemistry", "Chemical Reactivity"],
        "biology": ["Introduction to Biology", "Solving a Biological Problem", "Biodiversity", "Cells and Tissues", "Cell Cycle", "Enzymes", "Bioenergetics", "Nutrition", "Transport", "Coordination and Control"],
        "mathematics": ["Real Numbers", "Logarithms", "Sets and Functions", "Factorization and Algebraic Manipulation", "Linear Equations and Inequalities", "Trigonometry", "Coordinate Geometry", "Logic", "Similar Figures", "Graphs of Functions", "Loci and Construction", "Information Handling"],
    },
    10: {
        "physics": ["Simple Harmonic Motion and Waves", "Sound", "Geometrical Optics", "Electrostatics", "Current Electricity", "Electromagnetism", "Basic Electronics", "Information and Communication Technology", "Atomic and Nuclear Physics"],
        "chemistry": ["Chemical Equilibrium", "Acids, Bases and Salts", "Organic Chemistry", "Hydrocarbons", "Biochemistry", "Environmental Chemistry", "Water", "Chemical Industries"],
        "biology": ["Gaseous Exchange", "Homeostasis", "Coordination and Control", "Support and Movement", "Reproduction", "Inheritance", "Man and His Environment", "Biotechnology", "Pharmacology"],
        "mathematics": ["Quadratic Equations", "Theory of Quadratic Equations", "Variations", "Partial Fractions", "Sets and Functions", "Basic Statistics", "Introduction to Trigonometry", "Projection of a Side of Triangle", "Chords of a Circle", "Tangent to a Circle", "Practical Geometry", "Circle Measurement"],
    },
    11: {
        "physics": ["Measurements", "Vectors and Equilibrium", "Motion and Force", "Work and Energy", "Circular Motion", "Fluid Dynamics", "Oscillations", "Waves"],
        "chemistry": ["Basic Concepts", "Atomic Structure", "Chemical Bonding", "States of Matter", "Chemical Energetics", "Chemical Equilibrium", "Reaction Kinetics"],
        "biology": ["Introduction to Biology", "Biological Molecules", "Enzymes", "Cell Structure", "Variety of Life", "Kingdom Prokaryotae", "Kingdom Protista", "Kingdom Fungi", "Kingdom Plantae", "Kingdom Animalia"],
        "mathematics": ["Number Systems", "Sets and Functions", "Matrices and Determinants", "Quadratic Equations", "Partial Fractions", "Sequences and Series", "Permutations and Combinations", "Binomial Theorem", "Trigonometry", "Trigonometric Identities", "Trigonometric Functions"],
        "computer_science": ["Introduction to IT", "Data Representation", "Computer Architecture", "Operating Systems", "Programming Fundamentals", "Control Structures"],
    },
    12: {
        "physics": ["Electrostatics", "Current Electricity", "Capacitance", "Electromagnetism", "Electromagnetic Induction", "Alternating Current", "Physics of Solids", "Electronics", "Modern Physics", "Atomic Spectra", "Nuclear Physics"],
        "chemistry": ["Periodic Classification", "s-Block Elements", "p-Block Elements", "d-Block Elements", "Coordination Compounds", "Fundamental Principles of Organic Chemistry", "Hydrocarbons", "Alkyl Halides", "Alcohols and Phenols", "Aldehydes and Ketones", "Carboxylic Acids", "Macromolecules"],
        "biology": ["Homeostasis", "Support and Movement", "Coordination and Control", "Reproduction", "Growth and Development", "Chromosomes and DNA", "Cell Cycle", "Biotechnology", "Evolution", "Ecosystem"],
        "mathematics": ["Functions and Limits", "Differentiation", "Integration", "Differential Equations", "Complex Numbers", "Vectors", "Analytical Geometry", "Conic Sections"],
        "computer_science": ["Advanced Programming", "File Handling", "Data Structures", "Databases", "Networking"],
    },
}

# Static Marks Database — simulating what the marking app would save
# Structure: list of dicts with student_id, topic, date, obtained, total
MARKS_DB = []

def generate_static_marks():
    """Generate realistic static marks data for ALL students"""
    marks = []
    base_date = datetime(2025, 1, 15)

    def add_student_marks(student_id, class_section, subject, topic_performance):
        class_num = int(class_section.split('-')[0])
        topics = COURSE_OUTLINE.get(class_num, {}).get(subject.lower(), [])
        for topic_idx, topic in enumerate(topics):
            if topic not in topic_performance:
                continue
            performances = topic_performance[topic]
            for i, (obtained, total) in enumerate(performances):
                date = (base_date + timedelta(days=topic_idx * 7 + i * 3)).strftime("%Y-%m-%d")
                marks.append({
                    "student_id": student_id,
                    "topic": topic,
                    "date": date,
                    "obtained": obtained,
                    "total": total,
                })

    # ===================== 9-A =====================
    # Ahmed Khan — Mathematics (AT RISK in some)
    add_student_marks(1, "9-A", "mathematics", {
        "Real Numbers": [(3,5),(4,5),(2,3),(4,5)],
        "Logarithms": [(2,5),(2,5),(1,3),(2,5),(3,5)],
        "Sets and Functions": [(4,5),(5,5),(3,3),(4,5)],
        "Factorization and Algebraic Manipulation": [(3,5),(4,5),(2,3),(3,5)],
        "Linear Equations and Inequalities": [(4,5),(5,5),(3,3),(5,5)],
        "Trigonometry": [(2,5),(3,5),(1,3),(2,5)],
        "Coordinate Geometry": [(3,5),(4,5),(3,3)],
        "Logic": [(4,5),(5,5),(3,3)],
        "Similar Figures": [(3,5),(4,5),(2,3)],
        "Graphs of Functions": [(2,5),(3,5),(1,3)],
        "Loci and Construction": [(4,5),(5,5),(3,3)],
        "Information Handling": [(3,5),(4,5),(3,3)],
    })
    # Ahmed Khan — Physics
    add_student_marks(1, "9-A", "physics", {
        "Physical Quantities and Measurements": [(4,5),(5,5),(3,3)],
        "Kinematics": [(3,5),(4,5),(2,3)],
        "Dynamics": [(2,5),(3,5),(1,3)],
        "Turning Effect of Forces": [(3,5),(4,5),(2,3)],
        "Work, Energy and Power": [(4,5),(5,5),(3,3)],
        "Gravitation": [(3,5),(4,5),(2,3)],
        "Properties of Matter": [(4,5),(5,5),(3,3)],
        "Thermal Properties of Matter": [(3,5),(4,5),(2,3)],
        "Magnetism": [(2,5),(3,5),(1,3)],
        "Nature of Science": [(4,5),(5,5)],
    })
    # Fatima Ali — Biology (WEAK in Cells and Tissues)
    add_student_marks(2, "9-A", "biology", {
        "Introduction to Biology": [(4,5),(5,5),(3,3),(4,5)],
        "Solving a Biological Problem": [(3,5),(4,5),(2,3),(3,5)],
        "Biodiversity": [(2,5),(2,5),(1,3),(2,5),(3,5)],
        "Cells and Tissues": [(1,5),(2,5),(0,3),(1,5),(2,5),(1,3)],
        "Cell Cycle": [(3,5),(4,5),(2,3),(3,5)],
        "Enzymes": [(2,5),(3,5),(1,3),(2,5)],
        "Bioenergetics": [(3,5),(4,5),(2,3)],
        "Nutrition": [(4,5),(5,5),(3,3)],
        "Transport": [(3,5),(4,5),(2,3)],
        "Coordination and Control": [(2,5),(3,5),(1,3)],
    })
    # Fatima Ali — Chemistry
    add_student_marks(2, "9-A", "chemistry", {
        "Introduction to Chemistry": [(4,5),(5,5),(3,3)],
        "Structure of Atom": [(3,5),(4,5),(2,3)],
        "Periodic Table and Periodicity": [(4,5),(5,5),(3,3)],
        "Structure of Molecules": [(3,5),(4,5),(2,3)],
        "Physical States of Matter": [(4,5),(5,5),(3,3)],
        "Solutions": [(3,5),(4,5),(2,3)],
        "Electrochemistry": [(2,5),(3,5),(1,3)],
        "Chemical Reactivity": [(3,5),(4,5),(2,3)],
    })
    # Usman Raza — Physics (STRONG)
    add_student_marks(3, "9-A", "physics", {
        "Physical Quantities and Measurements": [(5,5),(5,5),(3,3),(5,5)],
        "Kinematics": [(4,5),(5,5),(3,3),(4,5)],
        "Dynamics": [(4,5),(5,5),(3,3),(5,5)],
        "Turning Effect of Forces": [(4,5),(5,5),(3,3),(4,5)],
        "Work, Energy and Power": [(5,5),(5,5),(3,3),(5,5)],
        "Gravitation": [(4,5),(5,5),(3,3),(4,5)],
        "Properties of Matter": [(4,5),(5,5),(3,3),(5,5)],
        "Thermal Properties of Matter": [(4,5),(5,5),(3,3),(4,5)],
        "Magnetism": [(4,5),(5,5),(3,3)],
        "Nature of Science": [(5,5),(5,5)],
    })
    # Ayesha Noor — Mathematics
    add_student_marks(4, "9-A", "mathematics", {
        "Real Numbers": [(4,5),(5,5),(3,3)],
        "Logarithms": [(3,5),(4,5),(2,3)],
        "Sets and Functions": [(4,5),(5,5),(3,3)],
        "Factorization and Algebraic Manipulation": [(3,5),(4,5),(2,3)],
        "Linear Equations and Inequalities": [(4,5),(5,5),(3,3)],
        "Trigonometry": [(3,5),(4,5),(2,3)],
        "Coordinate Geometry": [(4,5),(5,5),(3,3)],
        "Logic": [(4,5),(5,5),(3,3)],
        "Similar Figures": [(3,5),(4,5),(2,3)],
        "Graphs of Functions": [(3,5),(4,5),(2,3)],
        "Loci and Construction": [(4,5),(5,5),(3,3)],
        "Information Handling": [(4,5),(5,5),(3,3)],
    })
    # Bilal Ahmad — Chemistry (WEAK)
    add_student_marks(5, "9-A", "chemistry", {
        "Introduction to Chemistry": [(2,5),(3,5),(1,3),(2,5)],
        "Structure of Atom": [(1,5),(2,5),(0,3),(1,5),(2,5)],
        "Periodic Table and Periodicity": [(2,5),(3,5),(1,3),(2,5)],
        "Structure of Molecules": [(1,5),(2,5),(0,3),(1,5)],
        "Physical States of Matter": [(2,5),(3,5),(1,3),(2,5)],
        "Solutions": [(3,5),(4,5),(2,3),(3,5)],
        "Electrochemistry": [(2,5),(2,5),(1,3),(2,5)],
        "Chemical Reactivity": [(1,5),(2,5),(0,3),(1,5)],
    })
    # Zara Hussain — Biology
    add_student_marks(6, "9-A", "biology", {
        "Introduction to Biology": [(4,5),(5,5),(3,3)],
        "Solving a Biological Problem": [(4,5),(5,5),(3,3)],
        "Biodiversity": [(3,5),(4,5),(2,3)],
        "Cells and Tissues": [(4,5),(5,5),(3,3)],
        "Cell Cycle": [(3,5),(4,5),(2,3)],
        "Enzymes": [(4,5),(5,5),(3,3)],
        "Bioenergetics": [(3,5),(4,5),(2,3)],
        "Nutrition": [(4,5),(5,5),(3,3)],
        "Transport": [(3,5),(4,5),(2,3)],
        "Coordination and Control": [(4,5),(5,5),(3,3)],
    })

    # ===================== 9-B =====================
    # Hassan Javed — Mathematics
    add_student_marks(7, "9-B", "mathematics", {
        "Real Numbers": [(3,5),(4,5),(2,3)],
        "Logarithms": [(2,5),(3,5),(1,3)],
        "Sets and Functions": [(3,5),(4,5),(2,3)],
        "Factorization and Algebraic Manipulation": [(2,5),(3,5),(1,3)],
        "Linear Equations and Inequalities": [(3,5),(4,5),(2,3)],
        "Trigonometry": [(2,5),(3,5),(1,3)],
        "Coordinate Geometry": [(3,5),(4,5),(2,3)],
        "Logic": [(4,5),(5,5),(3,3)],
        "Similar Figures": [(3,5),(4,5),(2,3)],
        "Graphs of Functions": [(2,5),(3,5),(1,3)],
        "Loci and Construction": [(3,5),(4,5),(2,3)],
        "Information Handling": [(3,5),(4,5),(2,3)],
    })
    # Maryam Tariq — Physics (STRONG)
    add_student_marks(8, "9-B", "physics", {
        "Physical Quantities and Measurements": [(5,5),(5,5),(3,3),(5,5)],
        "Kinematics": [(4,5),(5,5),(3,3),(4,5)],
        "Dynamics": [(5,5),(5,5),(3,3),(5,5)],
        "Turning Effect of Forces": [(4,5),(5,5),(3,3),(4,5)],
        "Work, Energy and Power": [(5,5),(5,5),(3,3),(5,5)],
        "Gravitation": [(4,5),(5,5),(3,3),(4,5)],
        "Properties of Matter": [(5,5),(5,5),(3,3),(5,5)],
        "Thermal Properties of Matter": [(4,5),(5,5),(3,3),(4,5)],
        "Magnetism": [(4,5),(5,5),(3,3)],
        "Nature of Science": [(5,5),(5,5)],
    })
    # Omar Farooq — Chemistry
    add_student_marks(9, "9-B", "chemistry", {
        "Introduction to Chemistry": [(3,5),(4,5),(2,3)],
        "Structure of Atom": [(2,5),(3,5),(1,3)],
        "Periodic Table and Periodicity": [(3,5),(4,5),(2,3)],
        "Structure of Molecules": [(2,5),(3,5),(1,3)],
        "Physical States of Matter": [(3,5),(4,5),(2,3)],
        "Solutions": [(4,5),(5,5),(3,3)],
        "Electrochemistry": [(2,5),(3,5),(1,3)],
        "Chemical Reactivity": [(3,5),(4,5),(2,3)],
    })
    # Sana Iqbal — Biology (WEAK in Enzymes)
    add_student_marks(10, "9-B", "biology", {
        "Introduction to Biology": [(4,5),(5,5),(3,3)],
        "Solving a Biological Problem": [(3,5),(4,5),(2,3)],
        "Biodiversity": [(4,5),(5,5),(3,3)],
        "Cells and Tissues": [(3,5),(4,5),(2,3)],
        "Cell Cycle": [(4,5),(5,5),(3,3)],
        "Enzymes": [(1,5),(2,5),(0,3),(1,5),(2,5)],
        "Bioenergetics": [(3,5),(4,5),(2,3)],
        "Nutrition": [(4,5),(5,5),(3,3)],
        "Transport": [(3,5),(4,5),(2,3)],
        "Coordination and Control": [(4,5),(5,5),(3,3)],
    })
    # Imran Sheikh — Mathematics (AT RISK)
    add_student_marks(11, "9-B", "mathematics", {
        "Real Numbers": [(2,5),(3,5),(1,3),(2,5)],
        "Logarithms": [(2,5),(2,5),(1,3),(2,5)],
        "Sets and Functions": [(3,5),(4,5),(2,3)],
        "Factorization and Algebraic Manipulation": [(2,5),(3,5),(1,3)],
        "Linear Equations and Inequalities": [(3,5),(4,5),(2,3)],
        "Trigonometry": [(2,5),(2,5),(1,3),(2,5)],
        "Coordinate Geometry": [(3,5),(4,5),(2,3)],
        "Logic": [(4,5),(5,5),(3,3)],
        "Similar Figures": [(2,5),(3,5),(1,3)],
        "Graphs of Functions": [(2,5),(3,5),(1,3)],
        "Loci and Construction": [(3,5),(4,5),(2,3)],
        "Information Handling": [(3,5),(4,5),(2,3)],
    })

    # ===================== 10-A =====================
    # Ali Raza — Chemistry (WEAK in Chemical Equilibrium)
    add_student_marks(12, "10-A", "chemistry", {
        "Chemical Equilibrium": [(1,5),(2,5),(1,3),(2,5),(1,5),(2,5),(1,3),(2,5)],
        "Acids, Bases and Salts": [(4,5),(5,5),(3,3),(4,5),(5,5)],
        "Organic Chemistry": [(2,5),(3,5),(2,3),(3,5)],
        "Hydrocarbons": [(3,5),(4,5),(3,3),(4,5)],
        "Biochemistry": [(2,5),(2,5),(1,3),(2,5)],
        "Environmental Chemistry": [(4,5),(5,5),(4,3),(4,5)],
        "Water": [(3,5),(4,5),(3,3)],
        "Chemical Industries": [(2,5),(3,5),(2,3)],
    })
    # Ali Raza — Physics
    add_student_marks(12, "10-A", "physics", {
        "Simple Harmonic Motion and Waves": [(3,5),(4,5),(2,3)],
        "Sound": [(2,5),(3,5),(1,3)],
        "Geometrical Optics": [(3,5),(4,5),(2,3)],
        "Electrostatics": [(2,5),(3,5),(1,3)],
        "Current Electricity": [(3,5),(4,5),(2,3)],
        "Electromagnetism": [(2,5),(3,5),(1,3)],
        "Basic Electronics": [(3,5),(4,5)],
        "Information and Communication Technology": [(4,5),(5,5)],
        "Atomic and Nuclear Physics": [(2,5),(3,5)],
    })
    # Hira Khan — Chemistry (STRONG)
    add_student_marks(13, "10-A", "chemistry", {
        "Chemical Equilibrium": [(4,5),(5,5),(3,3),(4,5),(5,5),(4,5)],
        "Acids, Bases and Salts": [(5,5),(5,5),(3,3),(5,5),(4,5)],
        "Organic Chemistry": [(4,5),(5,5),(3,3),(4,5)],
        "Hydrocarbons": [(4,5),(5,5),(3,3),(5,5)],
        "Biochemistry": [(4,5),(5,5),(3,3),(4,5)],
        "Environmental Chemistry": [(5,5),(5,5),(3,3),(5,5)],
        "Water": [(4,5),(5,5),(3,3)],
        "Chemical Industries": [(4,5),(5,5),(3,3)],
    })
    # Saad Malik — Physics (AT RISK)
    add_student_marks(14, "10-A", "physics", {
        "Simple Harmonic Motion and Waves": [(3,5),(4,5),(2,3),(3,5)],
        "Sound": [(2,5),(3,5),(1,3),(2,5),(3,5)],
        "Geometrical Optics": [(4,5),(5,5),(3,3),(4,5)],
        "Electrostatics": [(2,5),(3,5),(1,3),(2,5),(3,5)],
        "Current Electricity": [(3,5),(4,5),(2,3),(3,5)],
        "Electromagnetism": [(2,5),(3,5),(1,3),(2,5)],
        "Basic Electronics": [(3,5),(4,5),(2,3)],
        "Information and Communication Technology": [(4,5),(5,5),(3,3)],
        "Atomic and Nuclear Physics": [(2,5),(3,5),(1,3)],
    })
    # Nida Fatima — Biology (WEAK in Homeostasis)
    add_student_marks(15, "10-A", "biology", {
        "Gaseous Exchange": [(4,5),(5,5),(3,3),(4,5)],
        "Homeostasis": [(2,5),(2,5),(1,3),(2,5),(1,5),(2,5)],
        "Coordination and Control": [(3,5),(4,5),(2,3),(3,5)],
        "Support and Movement": [(4,5),(5,5),(3,3),(4,5)],
        "Reproduction": [(2,5),(3,5),(1,3),(2,5)],
        "Inheritance": [(3,5),(4,5),(2,3),(3,5)],
        "Man and His Environment": [(4,5),(5,5),(3,3)],
        "Biotechnology": [(2,5),(3,5),(1,3)],
        "Pharmacology": [(3,5),(4,5),(2,3)],
    })
    # Waqar Ahmed — Mathematics
    add_student_marks(16, "10-A", "mathematics", {
        "Quadratic Equations": [(3,5),(4,5),(2,3)],
        "Theory of Quadratic Equations": [(2,5),(3,5),(1,3)],
        "Variations": [(3,5),(4,5),(2,3)],
        "Partial Fractions": [(2,5),(3,5),(1,3)],
        "Sets and Functions": [(3,5),(4,5),(2,3)],
        "Basic Statistics": [(4,5),(5,5),(3,3)],
        "Introduction to Trigonometry": [(2,5),(3,5),(1,3)],
        "Projection of a Side of Triangle": [(3,5),(4,5),(2,3)],
        "Chords of a Circle": [(2,5),(3,5),(1,3)],
        "Tangent to a Circle": [(3,5),(4,5),(2,3)],
        "Practical Geometry": [(4,5),(5,5),(3,3)],
        "Circle Measurement": [(3,5),(4,5),(2,3)],
    })
    # Rabia Sultana — Chemistry
    add_student_marks(17, "10-A", "chemistry", {
        "Chemical Equilibrium": [(3,5),(4,5),(2,3),(3,5)],
        "Acids, Bases and Salts": [(4,5),(5,5),(3,3),(4,5)],
        "Organic Chemistry": [(3,5),(4,5),(2,3)],
        "Hydrocarbons": [(4,5),(5,5),(3,3)],
        "Biochemistry": [(3,5),(4,5),(2,3)],
        "Environmental Chemistry": [(4,5),(5,5),(3,3)],
        "Water": [(3,5),(4,5),(2,3)],
        "Chemical Industries": [(4,5),(5,5),(3,3)],
    })
    # Tariq Mehmood — Physics (WEAK)
    add_student_marks(18, "10-A", "physics", {
        "Simple Harmonic Motion and Waves": [(2,5),(2,5),(1,3),(2,5)],
        "Sound": [(1,5),(2,5),(0,3),(1,5)],
        "Geometrical Optics": [(2,5),(3,5),(1,3),(2,5)],
        "Electrostatics": [(1,5),(2,5),(0,3),(1,5)],
        "Current Electricity": [(2,5),(3,5),(1,3),(2,5)],
        "Electromagnetism": [(1,5),(2,5),(0,3),(1,5)],
        "Basic Electronics": [(2,5),(3,5),(1,3)],
        "Information and Communication Technology": [(3,5),(4,5),(2,3)],
        "Atomic and Nuclear Physics": [(2,5),(2,5),(1,3)],
    })

    # ===================== 10-B =====================
    # Kamran Ali — Mathematics
    add_student_marks(19, "10-B", "mathematics", {
        "Quadratic Equations": [(3,5),(4,5),(2,3)],
        "Theory of Quadratic Equations": [(3,5),(4,5),(2,3)],
        "Variations": [(2,5),(3,5),(1,3)],
        "Partial Fractions": [(3,5),(4,5),(2,3)],
        "Sets and Functions": [(4,5),(5,5),(3,3)],
        "Basic Statistics": [(3,5),(4,5),(2,3)],
        "Introduction to Trigonometry": [(2,5),(3,5),(1,3)],
        "Projection of a Side of Triangle": [(3,5),(4,5),(2,3)],
        "Chords of a Circle": [(2,5),(3,5),(1,3)],
        "Tangent to a Circle": [(3,5),(4,5),(2,3)],
        "Practical Geometry": [(4,5),(5,5),(3,3)],
        "Circle Measurement": [(3,5),(4,5),(2,3)],
    })
    # Sadia Bibi — Biology
    add_student_marks(20, "10-B", "biology", {
        "Gaseous Exchange": [(4,5),(5,5),(3,3)],
        "Homeostasis": [(3,5),(4,5),(2,3)],
        "Coordination and Control": [(4,5),(5,5),(3,3)],
        "Support and Movement": [(3,5),(4,5),(2,3)],
        "Reproduction": [(4,5),(5,5),(3,3)],
        "Inheritance": [(3,5),(4,5),(2,3)],
        "Man and His Environment": [(4,5),(5,5),(3,3)],
        "Biotechnology": [(3,5),(4,5),(2,3)],
        "Pharmacology": [(4,5),(5,5),(3,3)],
    })
    # Noman Haider — Chemistry (AT RISK)
    add_student_marks(21, "10-B", "chemistry", {
        "Chemical Equilibrium": [(2,5),(3,5),(1,3),(2,5),(3,5)],
        "Acids, Bases and Salts": [(3,5),(4,5),(2,3),(3,5)],
        "Organic Chemistry": [(2,5),(3,5),(1,3),(2,5)],
        "Hydrocarbons": [(3,5),(4,5),(2,3),(3,5)],
        "Biochemistry": [(2,5),(3,5),(1,3),(2,5)],
        "Environmental Chemistry": [(3,5),(4,5),(2,3),(3,5)],
        "Water": [(2,5),(3,5),(1,3)],
        "Chemical Industries": [(3,5),(4,5),(2,3)],
    })
    # Fiza Khan — Physics
    add_student_marks(22, "10-B", "physics", {
        "Simple Harmonic Motion and Waves": [(4,5),(5,5),(3,3)],
        "Sound": [(3,5),(4,5),(2,3)],
        "Geometrical Optics": [(4,5),(5,5),(3,3)],
        "Electrostatics": [(3,5),(4,5),(2,3)],
        "Current Electricity": [(4,5),(5,5),(3,3)],
        "Electromagnetism": [(3,5),(4,5),(2,3)],
        "Basic Electronics": [(4,5),(5,5)],
        "Information and Communication Technology": [(4,5),(5,5)],
        "Atomic and Nuclear Physics": [(3,5),(4,5)],
    })
    # Shahid Afridi — Chemistry (WEAK in Organic Chemistry)
    add_student_marks(23, "10-B", "chemistry", {
        "Chemical Equilibrium": [(3,5),(4,5),(2,3),(3,5)],
        "Acids, Bases and Salts": [(4,5),(5,5),(3,3),(4,5)],
        "Organic Chemistry": [(1,5),(2,5),(0,3),(1,5),(2,5),(1,3)],
        "Hydrocarbons": [(2,5),(3,5),(1,3),(2,5)],
        "Biochemistry": [(3,5),(4,5),(2,3)],
        "Environmental Chemistry": [(4,5),(5,5),(3,3)],
        "Water": [(3,5),(4,5),(2,3)],
        "Chemical Industries": [(2,5),(3,5),(1,3)],
    })
    # Shahid Afridi — Physics
    add_student_marks(23, "10-B", "physics", {
        "Simple Harmonic Motion and Waves": [(2,5),(3,5),(1,3)],
        "Sound": [(3,5),(4,5),(2,3)],
        "Geometrical Optics": [(2,5),(3,5),(1,3)],
        "Electrostatics": [(3,5),(4,5),(2,3)],
        "Current Electricity": [(2,5),(3,5),(1,3)],
        "Electromagnetism": [(3,5),(4,5),(2,3)],
        "Basic Electronics": [(2,5),(3,5)],
        "Information and Communication Technology": [(3,5),(4,5)],
        "Atomic and Nuclear Physics": [(2,5),(3,5)],
    })

    # ===================== 11-Science-A =====================
    # Danish Tariq — Chemistry (WEAK in Reaction Kinetics)
    add_student_marks(24, "11-Science-A", "chemistry", {
        "Basic Concepts": [(4,5),(5,5),(3,3),(4,5)],
        "Atomic Structure": [(3,5),(4,5),(2,3),(3,5)],
        "Chemical Bonding": [(4,5),(5,5),(3,3),(4,5)],
        "States of Matter": [(3,5),(4,5),(2,3),(3,5)],
        "Chemical Energetics": [(2,5),(2,5),(1,3),(2,5),(1,5),(2,5)],
        "Chemical Equilibrium": [(3,5),(4,5),(2,3),(3,5),(4,5)],
        "Reaction Kinetics": [(1,5),(1,5),(0,3),(1,5),(2,5),(1,3),(1,5)],
    })
    # Amina Zahra — Physics (STRONG)
    add_student_marks(25, "11-Science-A", "physics", {
        "Measurements": [(5,5),(5,5),(3,3),(5,5),(4,5)],
        "Vectors and Equilibrium": [(4,5),(5,5),(3,3),(4,5),(5,5)],
        "Motion and Force": [(5,5),(5,5),(3,3),(5,5)],
        "Work and Energy": [(4,5),(5,5),(3,3),(4,5),(5,5)],
        "Circular Motion": [(4,5),(5,5),(2,3),(4,5)],
        "Fluid Dynamics": [(3,5),(4,5),(2,3),(3,5)],
        "Oscillations": [(4,5),(5,5),(3,3)],
        "Waves": [(4,5),(5,5),(3,3),(4,5)],
    })
    # Fahad Mustafa — Biology
    add_student_marks(26, "11-Science-A", "biology", {
        "Introduction to Biology": [(3,5),(4,5),(2,3)],
        "Biological Molecules": [(4,5),(5,5),(3,3)],
        "Enzymes": [(2,5),(3,5),(1,3)],
        "Cell Structure": [(3,5),(4,5),(2,3)],
        "Variety of Life": [(4,5),(5,5),(3,3)],
        "Kingdom Prokaryotae": [(3,5),(4,5),(2,3)],
        "Kingdom Protista": [(2,5),(3,5),(1,3)],
        "Kingdom Fungi": [(3,5),(4,5),(2,3)],
        "Kingdom Plantae": [(4,5),(5,5),(3,3)],
        "Kingdom Animalia": [(3,5),(4,5),(2,3)],
    })
    # Laiba Noor — Mathematics
    add_student_marks(27, "11-Science-A", "mathematics", {
        "Number Systems": [(4,5),(5,5),(3,3)],
        "Sets and Functions": [(3,5),(4,5),(2,3)],
        "Matrices and Determinants": [(4,5),(5,5),(3,3)],
        "Quadratic Equations": [(3,5),(4,5),(2,3)],
        "Partial Fractions": [(4,5),(5,5),(3,3)],
        "Sequences and Series": [(3,5),(4,5),(2,3)],
        "Permutations and Combinations": [(2,5),(3,5),(1,3)],
        "Binomial Theorem": [(3,5),(4,5),(2,3)],
        "Trigonometry": [(4,5),(5,5),(3,3)],
        "Trigonometric Identities": [(3,5),(4,5),(2,3)],
        "Trigonometric Functions": [(4,5),(5,5),(3,3)],
    })
    # Zain Abbas — Chemistry
    add_student_marks(28, "11-Science-A", "chemistry", {
        "Basic Concepts": [(3,5),(4,5),(2,3)],
        "Atomic Structure": [(2,5),(3,5),(1,3)],
        "Chemical Bonding": [(3,5),(4,5),(2,3)],
        "States of Matter": [(4,5),(5,5),(3,3)],
        "Chemical Energetics": [(2,5),(3,5),(1,3)],
        "Chemical Equilibrium": [(3,5),(4,5),(2,3)],
        "Reaction Kinetics": [(2,5),(3,5),(1,3)],
    })
    # Mehwish Hayat — Physics
    add_student_marks(29, "11-Science-A", "physics", {
        "Measurements": [(3,5),(4,5),(2,3)],
        "Vectors and Equilibrium": [(4,5),(5,5),(3,3)],
        "Motion and Force": [(3,5),(4,5),(2,3)],
        "Work and Energy": [(4,5),(5,5),(3,3)],
        "Circular Motion": [(3,5),(4,5),(2,3)],
        "Fluid Dynamics": [(2,5),(3,5),(1,3)],
        "Oscillations": [(3,5),(4,5),(2,3)],
        "Waves": [(4,5),(5,5),(3,3)],
    })

    # ===================== 11-Commerce-A =====================
    # Asif Ali — Computer Science (WEAK in Programming Fundamentals)
    add_student_marks(30, "11-Commerce-A", "computer_science", {
        "Introduction to IT": [(4,5),(5,5),(3,3),(4,5)],
        "Data Representation": [(3,5),(4,5),(2,3),(3,5)],
        "Computer Architecture": [(2,5),(2,5),(1,3),(2,5),(3,5)],
        "Operating Systems": [(3,5),(4,5),(2,3),(3,5)],
        "Programming Fundamentals": [(1,5),(2,5),(0,3),(1,5),(2,5),(1,3),(2,5)],
        "Control Structures": [(2,5),(3,5),(1,3),(2,5)],
    })
    # Nimra Khan — Computer Science
    add_student_marks(31, "11-Commerce-A", "computer_science", {
        "Introduction to IT": [(4,5),(5,5),(3,3)],
        "Data Representation": [(4,5),(5,5),(3,3)],
        "Computer Architecture": [(3,5),(4,5),(2,3)],
        "Operating Systems": [(4,5),(5,5),(3,3)],
        "Programming Fundamentals": [(3,5),(4,5),(2,3)],
        "Control Structures": [(4,5),(5,5),(3,3)],
    })
    # Rizwan Ahmed — Computer Science (AT RISK)
    add_student_marks(32, "11-Commerce-A", "computer_science", {
        "Introduction to IT": [(3,5),(4,5),(2,3)],
        "Data Representation": [(2,5),(3,5),(1,3)],
        "Computer Architecture": [(3,5),(4,5),(2,3)],
        "Operating Systems": [(2,5),(3,5),(1,3)],
        "Programming Fundamentals": [(3,5),(4,5),(2,3)],
        "Control Structures": [(2,5),(3,5),(1,3)],
    })
    # Saba Qamar — Computer Science (STRONG)
    add_student_marks(33, "11-Commerce-A", "computer_science", {
        "Introduction to IT": [(5,5),(5,5),(3,3),(5,5)],
        "Data Representation": [(4,5),(5,5),(3,3),(4,5)],
        "Computer Architecture": [(4,5),(5,5),(3,3),(5,5)],
        "Operating Systems": [(5,5),(5,5),(3,3),(5,5)],
        "Programming Fundamentals": [(4,5),(5,5),(3,3),(4,5)],
        "Control Structures": [(5,5),(5,5),(3,3),(5,5)],
    })

    # ===================== 12-Science-A =====================
    # Hamza Ali — Biology (Mixed)
    add_student_marks(34, "12-Science-A", "biology", {
        "Homeostasis": [(3,5),(4,5),(2,3),(3,5)],
        "Support and Movement": [(4,5),(5,5),(3,3),(4,5)],
        "Coordination and Control": [(2,5),(2,5),(1,3),(2,5),(3,5)],
        "Reproduction": [(3,5),(4,5),(2,3),(3,5)],
        "Growth and Development": [(4,5),(5,5),(3,3)],
        "Chromosomes and DNA": [(2,5),(3,5),(1,3),(2,5)],
        "Cell Cycle": [(3,5),(4,5),(2,3)],
        "Biotechnology": [(4,5),(5,5),(3,3)],
        "Evolution": [(3,5),(4,5),(2,3)],
        "Ecosystem": [(2,5),(3,5),(1,3)],
    })
    # Iqra Aziz — Chemistry
    add_student_marks(35, "12-Science-A", "chemistry", {
        "Periodic Classification": [(4,5),(5,5),(3,3)],
        "s-Block Elements": [(3,5),(4,5),(2,3)],
        "p-Block Elements": [(4,5),(5,5),(3,3)],
        "d-Block Elements": [(3,5),(4,5),(2,3)],
        "Coordination Compounds": [(4,5),(5,5),(3,3)],
        "Fundamental Principles of Organic Chemistry": [(3,5),(4,5),(2,3)],
        "Hydrocarbons": [(4,5),(5,5),(3,3)],
        "Alkyl Halides": [(3,5),(4,5),(2,3)],
        "Alcohols and Phenols": [(4,5),(5,5),(3,3)],
        "Aldehydes and Ketones": [(3,5),(4,5),(2,3)],
        "Carboxylic Acids": [(4,5),(5,5),(3,3)],
        "Macromolecules": [(3,5),(4,5),(2,3)],
    })
    # Babar Azam — Physics (STRONG)
    add_student_marks(36, "12-Science-A", "physics", {
        "Electrostatics": [(5,5),(5,5),(3,3),(5,5)],
        "Current Electricity": [(4,5),(5,5),(3,3),(4,5)],
        "Capacitance": [(5,5),(5,5),(3,3),(5,5)],
        "Electromagnetism": [(4,5),(5,5),(3,3),(4,5)],
        "Electromagnetic Induction": [(5,5),(5,5),(3,3),(5,5)],
        "Alternating Current": [(4,5),(5,5),(3,3),(4,5)],
        "Physics of Solids": [(5,5),(5,5),(3,3)],
        "Electronics": [(4,5),(5,5),(3,3)],
        "Modern Physics": [(5,5),(5,5),(3,3)],
        "Atomic Spectra": [(4,5),(5,5),(3,3)],
        "Nuclear Physics": [(5,5),(5,5),(3,3)],
    })
    # Maya Ali — Mathematics
    add_student_marks(37, "12-Science-A", "mathematics", {
        "Functions and Limits": [(3,5),(4,5),(2,3)],
        "Differentiation": [(4,5),(5,5),(3,3)],
        "Integration": [(3,5),(4,5),(2,3)],
        "Differential Equations": [(2,5),(3,5),(1,3)],
        "Complex Numbers": [(4,5),(5,5),(3,3)],
        "Vectors": [(3,5),(4,5),(2,3)],
        "Analytical Geometry": [(4,5),(5,5),(3,3)],
        "Conic Sections": [(3,5),(4,5),(2,3)],
    })
    # Shaheen Afridi — Biology (WEAK in Ecosystem)
    add_student_marks(38, "12-Science-A", "biology", {
        "Homeostasis": [(4,5),(5,5),(3,3)],
        "Support and Movement": [(3,5),(4,5),(2,3)],
        "Coordination and Control": [(4,5),(5,5),(3,3)],
        "Reproduction": [(3,5),(4,5),(2,3)],
        "Growth and Development": [(4,5),(5,5),(3,3)],
        "Chromosomes and DNA": [(3,5),(4,5),(2,3)],
        "Cell Cycle": [(4,5),(5,5),(3,3)],
        "Biotechnology": [(3,5),(4,5),(2,3)],
        "Evolution": [(4,5),(5,5),(3,3)],
        "Ecosystem": [(1,5),(2,5),(0,3),(1,5),(2,5)],
    })
    # Mahira Khan — Chemistry (AT RISK)
    add_student_marks(39, "12-Science-A", "chemistry", {
        "Periodic Classification": [(3,5),(4,5),(2,3)],
        "s-Block Elements": [(2,5),(3,5),(1,3)],
        "p-Block Elements": [(3,5),(4,5),(2,3)],
        "d-Block Elements": [(2,5),(3,5),(1,3)],
        "Coordination Compounds": [(3,5),(4,5),(2,3)],
        "Fundamental Principles of Organic Chemistry": [(2,5),(3,5),(1,3)],
        "Hydrocarbons": [(3,5),(4,5),(2,3)],
        "Alkyl Halides": [(2,5),(3,5),(1,3)],
        "Alcohols and Phenols": [(3,5),(4,5),(2,3)],
        "Aldehydes and Ketones": [(2,5),(3,5),(1,3)],
        "Carboxylic Acids": [(3,5),(4,5),(2,3)],
        "Macromolecules": [(2,5),(3,5),(1,3)],
    })

    # ===================== 12-Commerce-A =====================
    # Shoaib Akhtar — Computer Science
    add_student_marks(40, "12-Commerce-A", "computer_science", {
        "Advanced Programming": [(3,5),(4,5),(2,3)],
        "File Handling": [(2,5),(3,5),(1,3)],
        "Data Structures": [(3,5),(4,5),(2,3)],
        "Databases": [(4,5),(5,5),(3,3)],
        "Networking": [(3,5),(4,5),(2,3)],
    })
    # Hania Amir — Computer Science (STRONG)
    add_student_marks(41, "12-Commerce-A", "computer_science", {
        "Advanced Programming": [(5,5),(5,5),(3,3),(5,5)],
        "File Handling": [(4,5),(5,5),(3,3),(4,5)],
        "Data Structures": [(5,5),(5,5),(3,3),(5,5)],
        "Databases": [(4,5),(5,5),(3,3),(4,5)],
        "Networking": [(5,5),(5,5),(3,3),(5,5)],
    })
    # Wasim Akram — Computer Science (AT RISK)
    add_student_marks(42, "12-Commerce-A", "computer_science", {
        "Advanced Programming": [(2,5),(3,5),(1,3),(2,5)],
        "File Handling": [(3,5),(4,5),(2,3)],
        "Data Structures": [(2,5),(3,5),(1,3)],
        "Databases": [(3,5),(4,5),(2,3)],
        "Networking": [(2,5),(3,5),(1,3)],
    })
    # Sajal Aly — Computer Science
    add_student_marks(43, "12-Commerce-A", "computer_science", {
        "Advanced Programming": [(4,5),(5,5),(3,3)],
        "File Handling": [(3,5),(4,5),(2,3)],
        "Data Structures": [(4,5),(5,5),(3,3)],
        "Databases": [(3,5),(4,5),(2,3)],
        "Networking": [(4,5),(5,5),(3,3)],
    })

    return marks

MARKS_DB = generate_static_marks()

# ============================================================
# WEAKNESS DETECTION ALGORITHM (7 Steps)
# ============================================================

def detect_topic_weakness(topic_name, questions, lambda_decay=0.8):
    """
    Runs all 7 steps for one student + one topic.
    Input:  topic_name (str), questions (list of dicts with date, obtained, total)
    Output: result dict with status, score, trend, questions
    """

    # STEP 1 — Calculate percentage for each question
    for q in questions:
        q["percentage"] = (q["obtained"] / q["total"]) * 100

    # STEP 2 — Sort by date (oldest first), assign position
    questions = sorted(questions, key=lambda q: q["date"])
    for i, q in enumerate(questions):
        q["position"] = i + 1

    # STEP 3 — Calculate recency weight
    total = len(questions)
    for q in questions:
        exponent = total - q["position"]
        q["recency_weight"] = lambda_decay ** exponent

    # STEP 4 — Multiply percentage by weight
    for q in questions:
        q["weighted_score"] = q["percentage"] * q["recency_weight"]

    # STEP 5 — Calculate final topic score S
    sum_weighted_scores = sum(q["weighted_score"] for q in questions)
    sum_weights = sum(q["recency_weight"] for q in questions)
    S = sum_weighted_scores / sum_weights if sum_weights > 0 else 0

    # STEP 6 — Detect trend
    percentages = [q["percentage"] for q in questions]
    if len(percentages) < 2:
        trend = 0
        trend_label = "STABLE"
    else:
        midpoint = len(percentages) // 2
        older_half = percentages[:midpoint]
        newer_half = percentages[midpoint:]
        older_avg = sum(older_half) / len(older_half)
        newer_avg = sum(newer_half) / len(newer_half)
        trend = newer_avg - older_avg

        if trend > 10:
            trend_label = "IMPROVING"
        elif trend < -10:
            trend_label = "DECLINING"
        else:
            trend_label = "STABLE"

    # STEP 7 — Two gate checks
    question_count = len(questions)

    # Gate 1 — minimum questions
    if question_count < 3:
        return {
            "topic": topic_name,
            "status": "INSUFFICIENT DATA",
            "score": round(S, 2),
            "trend": trend_label,
            "questions": question_count,
            "trend_value": round(trend, 2),
        }

    # Gate 2 — score threshold
    if S < 50:
        status = "WEAK"
    elif S < 65:
        status = "AT RISK"
    else:
        status = "STRONG"

    return {
        "topic": topic_name,
        "status": status,
        "score": round(S, 2),
        "trend": trend_label,
        "questions": question_count,
        "trend_value": round(trend, 2),
    }


# ============================================================
# STREAMLIT UI
# ============================================================

st.title("🎯 Topic Weakness Detector")
st.markdown("Analyze student performance topic-by-topic to identify weak areas")
st.markdown("---")

# Session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# ── STEP 1: Select Class ──
st.subheader("1️⃣ Select Class")
all_classes = list(STUDENTS_DB.keys())
selected_class = st.selectbox("Choose Class & Section", ["-- Select Class --"] + all_classes, index=0)

if selected_class == "-- Select Class --":
    st.info("👆 Please select a class to continue")
    st.stop()

# ── STEP 2: Select Student ──
st.subheader("2️⃣ Select Student")
students = STUDENTS_DB.get(selected_class, [])
student_options = {f"{s['roll_no']} - {s['name']}": s for s in students}
selected_student_label = st.selectbox(
    f"Choose Student from {selected_class}",
    ["-- Select Student --"] + list(student_options.keys()),
    index=0
)

if selected_student_label == "-- Select Student --":
    st.info("👆 Please select a student to continue")
    st.stop()

selected_student = student_options[selected_student_label]

# ── STEP 3: Select Subject ──
st.subheader("3️⃣ Select Subject")
class_num = int(selected_class.split('-')[0])
available_subjects = list(COURSE_OUTLINE.get(class_num, {}).keys())
subject_options = [s.title().replace("_", " ") for s in available_subjects]
subject_display_to_key = {s.title().replace("_", " "): s for s in available_subjects}

selected_subject_display = st.selectbox(
    "Choose Subject",
    ["-- Select Subject --"] + subject_options,
    index=0
)

if selected_subject_display == "-- Select Subject --":
    st.info("👆 Please select a subject to continue")
    st.stop()

selected_subject = subject_display_to_key[selected_subject_display]

# ── STEP 4: Analyze ──
st.markdown("---")

if st.button("🔍 Analyze Weakness", type="primary", use_container_width=True):
    with st.spinner("Analyzing topic-wise performance..."):

        # Get all topics for this class + subject
        all_topics = COURSE_OUTLINE.get(class_num, {}).get(selected_subject, [])

        # Filter marks for this student
        student_marks = [m for m in MARKS_DB if m["student_id"] == selected_student["id"]]

        # Group marks by topic
        results = []
        for topic in all_topics:
            topic_marks = [m for m in student_marks if m["topic"] == topic]

            if topic_marks:
                result = detect_topic_weakness(topic, topic_marks)
            else:
                result = {
                    "topic": topic,
                    "status": "NO DATA",
                    "score": 0,
                    "trend": "—",
                    "questions": 0,
                    "trend_value": 0,
                }
            results.append(result)

        st.session_state.analysis_results = results

# ── Display Results ──
if st.session_state.analysis_results:
    results = st.session_state.analysis_results

    st.markdown("---")
    st.subheader(f"📊 Analysis Results: {selected_student['name']} — {selected_subject_display}")

    # Summary cards
    weak_count = sum(1 for r in results if r["status"] == "WEAK")
    at_risk_count = sum(1 for r in results if r["status"] == "AT RISK")
    strong_count = sum(1 for r in results if r["status"] == "STRONG")
    no_data_count = sum(1 for r in results if r["status"] in ["NO DATA", "INSUFFICIENT DATA"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Topics", len(results))
    c2.metric("🔴 Weak", weak_count)
    c3.metric("🟡 At Risk", at_risk_count)
    c4.metric("🟢 Strong", strong_count)
    c5.metric("⚪ No Data", no_data_count)

    st.markdown("---")

    # Create DataFrame for display
    df_results = pd.DataFrame(results)

    # Color coding function
    def color_status(val):
        if val == "WEAK":
            return "background-color: #ffcccc; color: #cc0000; font-weight: bold"
        elif val == "AT RISK":
            return "background-color: #fff3cd; color: #856404; font-weight: bold"
        elif val == "STRONG":
            return "background-color: #d4edda; color: #155724; font-weight: bold"
        elif val == "INSUFFICIENT DATA":
            return "background-color: #e2e3e5; color: #383d41"
        else:
            return "background-color: #f8f9fa; color: #6c757d"

    def color_score(val):
        if val == 0:
            return ""
        elif val < 50:
            return "color: #cc0000; font-weight: bold"
        elif val < 65:
            return "color: #856404; font-weight: bold"
        else:
            return "color: #155724; font-weight: bold"

    # Display styled table
    display_df = df_results[["topic", "score", "status", "trend", "questions"]].copy()
    display_df.columns = ["Topic", "Score (%)", "Status", "Trend", "Questions Answered"]

    styled_df = display_df.style        .map(color_status, subset=["Status"])        .map(color_score, subset=["Score (%)"])        .format({"Score (%)": "{:.1f}%"})

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # Bar chart
    st.markdown("---")
    st.subheader("📈 Topic-wise Score Comparison")

    chart_df = df_results[df_results["status"] != "NO DATA"].copy()
    if not chart_df.empty:
        chart_df = chart_df.sort_values("score", ascending=True)

        # Create color list based on status
        colors = []
        for _, row in chart_df.iterrows():
            if row["status"] == "WEAK":
                colors.append("#dc3545")  # red
            elif row["status"] == "AT RISK":
                colors.append("#ffc107")  # yellow
            elif row["status"] == "STRONG":
                colors.append("#28a745")  # green
            else:
                colors.append("#6c757d")  # gray

        chart_data = chart_df.set_index("topic")[["score"]]
        chart_data.columns = ["Score (%)"]

        st.bar_chart(chart_data)

    # Weak topics detail section
    st.markdown("---")
    weak_topics = [r for r in results if r["status"] == "WEAK"]
    at_risk_topics = [r for r in results if r["status"] == "AT RISK"]

    if weak_topics:
        st.subheader("🔴 Weak Topics — Need Immediate Attention")
        for r in weak_topics:
            with st.container():
                col_a, col_b, col_c = st.columns([3, 1, 1])
                col_a.markdown(f"**{r['topic']}**")
                col_b.markdown(f"Score: **{r['score']:.1f}%**")
                trend_emoji = "📈" if r["trend"] == "IMPROVING" else "📉" if r["trend"] == "DECLINING" else "➡️"
                col_c.markdown(f"Trend: {trend_emoji} {r['trend']}")
                st.progress(min(r["score"] / 100, 1.0))
                if r["trend"] == "DECLINING":
                    st.caption("⚠️ Performance is getting worse — urgent intervention needed!")
                elif r["trend"] == "IMPROVING":
                    st.caption("✅ Showing improvement — continue supporting practice")
                else:
                    st.caption("📌 Consistently weak — regular revision advised")
                st.markdown("---")

    if at_risk_topics:
        st.subheader("🟡 At Risk Topics — Need Focus")
        for r in at_risk_topics:
            with st.container():
                col_a, col_b, col_c = st.columns([3, 1, 1])
                col_a.markdown(f"**{r['topic']}**")
                col_b.markdown(f"Score: **{r['score']:.1f}%**")
                trend_emoji = "📈" if r["trend"] == "IMPROVING" else "📉" if r["trend"] == "DECLINING" else "➡️"
                col_c.markdown(f"Trend: {trend_emoji} {r['trend']}")
                st.progress(min(r["score"] / 100, 1.0))
                st.markdown("---")

    if not weak_topics and not at_risk_topics:
        st.success("🎉 Great! No weak or at-risk topics found for this student in this subject.")

    # Download report button
    st.markdown("---")
    report_df = df_results[["topic", "score", "status", "trend", "questions", "trend_value"]].copy()
    report_df.columns = ["Topic", "Score (%)", "Status", "Trend", "Questions", "Trend Value"]
    csv = report_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Report as CSV",
        data=csv,
        file_name=f"weakness_report_{selected_student['name']}_{selected_subject_display}.csv",
        mime="text/csv"
    )