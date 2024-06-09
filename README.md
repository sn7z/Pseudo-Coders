AI-Resume Insight:-

The problem AI-Resume Insight solves:
Our tool extracts essential information from resumes and provides an option to build a new resume if one is not available. After uploading a resume, it delivers the extracted data and offers smart, generative AI suggestions. Additionally, users can input queries in our generative AI chatbox and receive instant responses.

Challenges we ran into:
Finding and implementing a suitable generative AI API for our project was a tough journey. We needed an API that fit our model and gave good, relevant responses.
Learning HTML, CSS, JavaScript, and Flask for the first time was really hard. We faced many challenges and had to put in a lot of effort. There were times we felt stuck and unsure if we could continue.
But through hard work and teamwork, we built a website that looks good and works well. Our goal was to create something that helps society, and we are proud that we made it happen despite the difficulties.
This project shows our determination and the power of working together to overcome struggles and we tried our very best. and made new things and learned new things, and this event inspiried us to attend more upcoming hackathons and strive to get better and aim for the first position

AI-Resume Insight is an advanced AI-driven tool designed to extract essential data from resumes and offer personalized career suggestions. It also provides an option to generate resumes for users who do not have one. By leveraging generative AI, the system delivers smart insights and instant responses to queries, enhancing the resume creation and review process.


Table of Contents:
Features
Getting Started
Prerequisites
Installation
Usage
Project Structure
API Endpoints
Customization
Contributing
License
Contact

Features-
Resume Parsing: Extracts key information from uploaded resumes, such as name, contact details, skills, education, and work experience.
Resume Generation: Provides an easy-to-use form to generate a resume from scratch.
Generative AI Suggestions: Offers personalized career suggestions and improvements based on extracted resume data.
Instant AI Query Response: Users can ask questions and get instant replies from the AI.
User-Friendly Interface: A modern, responsive web interface designed for seamless user experience.

Getting Started-
Prerequisites:
Before you begin, ensure you have the following installed on your machine:

Python 3.8+
Node.js (for frontend development)
pip (Python package installer)
npm or yarn (for managing frontend dependencies)

Installation:
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/AI-Resume-Insight.git
cd AI-Resume-Insight
Backend Setup:

Navigate to the backend directory and install dependencies:
bash
Copy code
cd backend
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install Flask fpdf spacy pdfminer.six google-generative-ai
python -m spacy download en_core_web_sm
pip install Flask fpdf spacy pdfminer.six google-generative-ai && python -m spacy download en_core_web_sm
pip install google ai sdk

Frontend Setup:

Navigate to the frontend directory and install dependencies:
bash
Copy code
cd ../frontend
npm install
npm run build
Database Setup:

Ensure your database (e.g., PostgreSQL, SQLite) is running and accessible. Update config.py or .env with your database credentials.

Run the Application:

Start the backend server:

bash
Copy code
cd ../backend
flask run
Start the frontend server:

bash
Copy code
cd ../frontend
npm start
Access the Application:

Open your browser and go to http://localhost:3000 to access the AI-Resume Insight interface.

Usage-
Upload Resume:

Upload your resume in PDF format using the upload section. The system will extract the data and display it along with personalized suggestions.

Generate Resume:

Use the resume generation form to create a new resume. Fill in your details, and the system will generate a professional-looking resume.

Ask Queries:

Enter your questions or prompts in the AI chatbox to get instant responses based on the resume data and your inputs.

Project Structure
plaintext
Copy code
 
Structure- 
env/Parser folder =  app.py
                     index.html
                     staticfolder/logo.jpg
                     uploads folder

API Endpoints-
Backend
POST /upload: Upload a resume in PDF format for data extraction.
POST /generate_pdf: Generate a resume from user-provided details.
POST /generate: Get AI responses based on user prompts.
Frontend
/: Home page with resume upload and generation options.
/generate: AI chat interface for querying.
Customization
Styling: Update the CSS files in the frontend/src directory to customize the look and feel.
AI Models: Modify the AI models and logic in the backend to improve or change the AI suggestions.

Contributing-
We welcome contributions! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Create a new Pull Request.

License-
This project is licensed under the MIT License - see the LICENSE file for details.

Contact-
For any inquiries or support, please contact syednumaan15@gmail.com
