# CyberGuard: AI-Powered Cybersecurity Awareness Chatbot

CyberGuard is a web-based chatbot developed to improve cybersecurity awareness. It educates users on threats like phishing, malware, and ransomware, offers real-time alerts, answers queries, and provides interactive quizzes for learning.

---

## 🔍 Features

- AI-powered chatbot using RAG / OpenAI API / Rasa
- Educates users about cybersecurity threats
- Provides security tips and best practices
- Real-time alerts from cyber threat intelligence APIs (e.g., VirusTotal, AbuseIPDB)
- Interactive quizzes for learning reinforcement
- Secure web interface with HTTPS support

---

## 🛠️ Tech Stack

**Frontend:**  
- HTML, CSS, JavaScript

**Backend:**  
- Python (Flask)

**Chatbot Engine:**  
- RAG / OpenAI API / Rasa

**Database:**  
- SQLite

**APIs Used:**  
- VirusTotal, AbuseIPDB

**Hosting:**  
- Heroku / AWS

---

## 📐 System Architecture

**Three-Tier Architecture:**
- **Presentation Layer:** Web UI for user interaction
- **Application Layer:** Flask backend + Chatbot engine
- **Data Layer:** Database for quizzes, logs, and threat data

**Flow:**
1. User submits a query via the chat interface  
2. Chatbot processes input using NLP  
3. Relevant data fetched from DB or APIs  
4. Response displayed to the user

---

## 🧪 Testing Summary

- **Static Code Analysis:**  
  - Tools: Pylint, Flake8  
  - No critical errors, minor formatting warnings  
  - Code follows PEP8

- **Network Monitoring (Wireshark):**  
  - HTTPS used for all traffic  
  - No unencrypted sensitive data  
  - Minimal API calls for efficiency

- **Function Testing:**  
  - Handled 100+ queries with 95% accuracy  
  - Topics: phishing, malware, passwords, social engineering

---

## 🚀 Future Enhancements

- Better understanding using advanced NLP  
- Add regional/global language support  
- Live cyber threat updates via real-time feeds  
- Interactive learning modules and gamified quizzes  
- User profiles for progress tracking  
- Mobile app (Android/iOS)  
- Voice input/output for accessibility

---

## 📂 Project Structure

cyberguard/
├── static/ # CSS, JavaScript files
├── templates/ # HTML templates
├── chatbot/ # NLP logic and chatbot engine
├── app.py # Main Flask backend
├── database.db # SQLite database
└── requirements.txt # Python dependencies
