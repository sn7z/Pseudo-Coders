from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
import os
import re
import spacy
from spacy.matcher import Matcher, PhraseMatcher
from pdfminer.high_level import extract_text
from fpdf import FPDF
import google.generativeai as genai

genai.configure(api_key="your api key")
model = genai.GenerativeModel('gemini-1.5-flash')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['STATIC_FOLDER']):
    os.makedirs(app.config['STATIC_FOLDER'])

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(resume_text)

    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number

def extract_email_from_resume(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    matches = re.findall(pattern, text)
    return matches

def extract_skills_from_resume(text, skills_list):
    return [skill for skill in skills_list if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]

skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management',
               'Deep Learning', 'SQL', 'Tableau', 'Java', 'JavaScript', 'Ethical Hacking', 'Operating system',
               'os', 'C++', 'Ruby', 'Django', 'React', 'Angular', 'Coding', 'PHP', 'Swift', 'Go', 'Golang', 'Rust',
               'Kotlin', 'C#', 'Spring', 'Express.js', 'HTML', 'CSS', 'Vue.js', 'MySQL', 'Express', 'API', 'Git',
               'Git Hub', 'DevOps', 'Azure', 'AWS', 'Critical Thinking', 'Problem-Solving', 'Teamwork', 'Leadership',
               'R', 'IT', 'CI/CDI', 'Data Visualization', 'Ethereum', 'design', 'Hyperledger', 'Fabric', 'EOS',
               'Mathematics', 'Business', 'CA', 'NLP', 'Aerospace', 'Network', '.Net', 'Spring', 'Spring Boot',
               'Flutter', 'Flask', 'Gaming', 'Node.js', 'TypeScript', 'Dart', 'Matlab', 'Shell', 'Swift', 'Scala',
               'Pytorch', 'Tensor Flow', 'Cybersecurity', 'Robotics', 'Internet of Things', 'IoT', 'Mobile Development',
               'Web Development', 'Cloud Computing', 'Virtual Reality', 'VR',  'Augmented Reality', 'AR',
               'Game Development', 'Data Engineering', 'Natural Language Processing (NLP)', 'Computer Vision',
               'Blockchain Development', 'Quantum Computing', '3D Printing', 'CAD', 'CAM', 'Finite Element Analysis',
               'Digital Signal Processing (DSP)', 'Embedded Systems', 'Control Systems', 'Renewable Energy Systems']

def extract_education_from_resume(text):
    # Define patterns for academic fields and branches
    fields = [
        'Computer Science', 'CSE', 'ECE', 'EEE', 'Mechanical', 'BSE', 'BCA', 'BE', 'ME', 'Btech', 'Mtech',
        'Electrical', 'Civil', 'Chemical', 'Biomedical', 'Software Engineering', 'B.tech', 'M.tech'
        'Information Technology', 'IT', 'Aerospace', 'Environmental', 'Industrial',
        'Materials Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'MBBS', 'MD', 'PhD',
        'Business Administration', 'BBA', 'MBA', 'Finance', 'Marketing', 'Human Resources',
        'Philosophy', 'History', 'Psychology', 'Political Science', 'Sociology', 'AI', 'ML', 'Machine Learning',
        'Artificial Intelligence', 'Data Science', 'CSM', 'CSD', 'MEC', 'CS', 'IoT',
        'Geology', 'Environmental Science', 'Astronomy', 'Biotechnology', 'Genetics', 'Nanotechnology', 'Robotics',
        'Cybersecurity', 'Information Systems', 'Game Development', 'Graphic Design', 'User Experience Design',
        'Industrial Design', 'Fashion Design', 'Interior Design', 'Animation', 'Film Studies', 'Performing Arts',
        'Music Production', 'Journalism', 'Communication Studies', 'Event Management'
    ]
    fields_pattern = '|'.join([re.escape(field) for field in fields])
    pattern = rf"(?i)\b(?:B\.\w+|\bM\.\w+|\bB\w+|\bM\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\b\s*(?:in\s*)?({fields_pattern})"
    matches = re.findall(pattern, text)
    return [match.strip() for match in matches]

def extract_college_names(text):
    pattern = r"(?i)\b(?:University|College|Institute|Academy|School|Polytechnic|Center for|Faculty of)\s(?:of\s)?(?:\w+\s)*\w+\b"
    return [match.strip() for match in re.findall(pattern, text)]

def extract_work_experience(text):
    pattern = r"\b(\d+\s+years?)\b"
    years_phrases = re.findall(pattern, text)
    return years_phrases if years_phrases else None

def extract_job_roles(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    job_titles = [
        "Data Scientist", "Machine Learning Engineer", "Software Engineer", "Project Manager",
        "Data Analyst", "Business Analyst", "Consultant", "Research Scientist", "Developer",
        "UX/UI Designer", "Marketing Manager", "Sales Manager", "Financial Analyst",
        "Operations Manager", "Network Engineer", "Database Administrator", "Web Developer",
        "Frontend Developer", "Backend Developer", "Full Stack Developer", "Security Analyst",
        "Technical Writer", "Graphic Designer", "Account Manager", "Research Analyst",
        "Architect", "Civil Engineer", "Mechanical Engineer", "Electrical Engineer",
        "Chemical Engineer", "Environmental Scientist", "Physicist", "Chemist", "Biologist",
        "Nurse", "Physician", "Teacher", "Professor", 'web dev', 'dev', 'developer', 'designer'
    ]
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(title.lower()) for title in job_titles]
    matcher.add("JOB_ROLE", patterns)
    matches = matcher(doc)
    roles = [doc[start:end].text for match_id, start, end in matches]
    return list(set(roles))

def generate_suggestions(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return str(e)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            text = extract_text_from_pdf(file_path)
            text_file_path = file_path.replace('.pdf', '.txt')
            save_text_to_file(text, text_file_path)
        except Exception as e:
            return jsonify(error=f"Error extracting text from PDF: {e}"), 500

        name = extract_name(text) or "N/A"
        contact_number = extract_contact_number_from_resume(text) or "N/A"
        email = extract_email_from_resume(text) or "N/A"
        extracted_skills = extract_skills_from_resume(text, skills_list)
        extracted_education = extract_education_from_resume(text)
        extracted_work_experience = extract_work_experience(text)
        extracted_colleges = extract_college_names(text)
        extracted_job_roles = extract_job_roles(text)

        prompt = f" i am proficient in Skills: {', '.join(extracted_skills)}\n" \
                 f"and i want to become {', '.join(extracted_job_roles)}\n" \
                 f"What additional skills, languages, or courses could I learn to improve in this field?" \
                 f"Keep your response under 200 words and dont use bold font"

        suggestion = generate_suggestions(prompt)

        response = {
            'name': name,
            'contact_number': contact_number,
            'email': email,
            'skills': extracted_skills,
            'education': extracted_education,
            'work_experience': extracted_work_experience,
            'colleges': extracted_colleges,
            'job_roles': extracted_job_roles,
            'suggestion': suggestion,
            'text_file': text_file_path
        }

        return jsonify(response)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    full_name = request.form['full_name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    skills = request.form['skills']
    education = request.form['education']
    work_experience = request.form['work_experience']
    colleges = request.form['colleges']
    job_roles = request.form['job_roles']

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 14)
            self.set_fill_color(50, 50, 255)  # Dark Blue Background
            self.set_text_color(255, 255, 255)  # White text
            self.cell(0, 12, 'Resume', 0, 1, 'C', 1)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        def section_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.set_fill_color(240, 240, 240)  # Light Gray Background
            self.set_text_color(50, 50, 255)  # Dark Blue text
            self.cell(0, 10, title, 0, 1, 'L', 1)
            self.ln(2)

        def section_body(self, body):
            self.set_font('Arial', '', 12)
            self.set_text_color(0, 0, 0)  # Black text
            self.multi_cell(0, 10, body)
            self.ln(5)

        def personal_info(self, name, phone, email):
            self.set_font('Arial', 'B', 16)
            self.set_text_color(50, 50, 255)  # Dark Blue text
            self.cell(0, 10, name, 0, 1, 'C')
            self.set_font('Arial', '', 12)
            self.cell(0, 10, phone, 0, 1, 'C')
            self.cell(0, 10, email, 0, 1, 'C')
            self.ln(10)

    pdf = PDF()
    pdf.add_page()

    pdf.section_title('Name')
    pdf.section_body(full_name)

    pdf.section_title('Contact Number')
    pdf.section_body(phone_number)

    pdf.section_title('Email')
    pdf.section_body(email)

    pdf.section_title('Skills')
    pdf.section_body(skills)

    pdf.section_title('Academic Field')
    pdf.section_body(education)

    pdf.section_title('Year of Experience')
    pdf.section_body(work_experience)

    pdf.section_title('Job Roles')
    pdf.section_body(job_roles)

    pdf.section_title('College')
    pdf.section_body(colleges)

    pdf_path = os.path.join('uploads', f"{full_name.replace(' ', '_')}.pdf")
    pdf.output(pdf_path)

    return jsonify({"pdf_path": pdf_path})

@app.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return jsonify({'response': response.text})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
