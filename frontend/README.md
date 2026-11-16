
# AI Career Assistant 🚀

An AI-powered career guidance platform built using React, Django, MySQL, and Google Gemini AI.

## Features

- Resume PDF Upload
- AI-Based Resume Analysis
- Job Search Across India
- AI Job Recommendations
- Resume-Based Job Matching
- AI Career Roadmap
- AI Chatbot for Career Guidance
- Chat History Stored in MySQL
- Clear Chat Option
- Responsive Design for Mobile and Desktop

## Technologies Used

### Frontend
- React.js
- Vite
- JavaScript
- HTML
- CSS

### Backend
- Python
- Django
- REST API

### Database
- MySQL

### AI & APIs
- Google Gemini API
- SerpApi (Google Jobs Search)
- PyPDF2

## Project Structure

```text
AI_Career_Assistant/
│
├── backend/
│   ├── ai_engine/
│   ├── config/
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Career_Assistant
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the backend folder and configure:

```env
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_KEY=your_serpapi_key
```

Configure your MySQL database settings in Django.

**Never upload your actual API keys or passwords to GitHub.**

## Author

AI Career Assistant Project

## License

This project is created for learning and portfolio purposes.
