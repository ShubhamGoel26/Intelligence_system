# 🚀 AI Lead Intelligence System

An end-to-end **AI-powered lead generation system** that transforms raw company lists into enriched business insights, contact details, and personalized outreach messages.

Built using **FastAPI**, **CrewAI multi-agent architecture**, and a **Next.js frontend**.

---

## 🧠 What This Project Does

Upload an Excel file containing company data → the system:

1. 🔍 Researches the company using web data  
2. 📞 Finds contact details (email, phone, WhatsApp)  
3. ✍️ Generates personalized outreach messages  
4. ⚡ Runs everything in parallel for speed  

---

## 🏗️ Architecture Overview

Multi-agent pipeline:

Excel → Scraper → Research Agent → Contact Agent → Outreach Agent → Output

---

## 📁 Project Structure

.
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── llm.py
│   │   ├── agents/
│   │   ├── services/
│   │   └── models/
│   ├── requirements.txt
│   └── temp/
├── lead-intel-frontend/
└── README.md

---

## ⚙️ Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Create `.env`:

GOOGLE_API_KEY=your_key

Run server:

```bash
uvicorn backend.app.main:app --reload
```

---

## 📤 API Usage

POST /upload

Returns enriched company data with profile, contacts, and outreach message.

---

## 🌐 Frontend Setup

```bash
cd lead-intel-frontend
npm install
npm run dev
```

---

## 🔧 Tech Stack

- FastAPI
- CrewAI
- LangChain
- Google Gemini
- Pandas
- BeautifulSoup
- DuckDuckGo Search
- Next.js
- React
- Tailwind CSS

---

## ⚠️ Notes

- Do not commit `.env`
- Rotate API keys if exposed
- Data depends on public sources

---

## 👨‍💻 Author

Shubham Goel
