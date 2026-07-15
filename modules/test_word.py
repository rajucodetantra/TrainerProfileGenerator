from pathlib import Path
from word_generator import WordGenerator

print("Current Working Directory:", Path.cwd())

template = "templates/Trainer_Profile_Template.docx"

trainer = {
    "Name": "Jathin Kumar Chilamakuri",
    "Emp ID": "CT0755",
    "Designation": "Technical Trainer",
    "Company Mail": "jathinc@codetantra.in",
    "Phone Number": "6300435064",
    "Summary": "Sample Professional Summary",
    "Skills": "Python, Java, DSA",
    "Experience": "1 Year",
    "Rating": "4"
}

generator = WordGenerator(template, trainer)

generator.generate("output/DOCX/Test_Profile.docx")