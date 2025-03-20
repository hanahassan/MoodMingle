# MoodMingle
## SENG401 Final Project

---

### **For LLM Use**
```bash
pip install -q -U google-genai
```

---

### **Requirements**

#### Backend (Flask & MySQL)
```bash
pip install mysql-connector-python flask flask-cors python-dotenv
```

#### Frontend (React)
```bash
npm install react
npm install react-router-dom
npm install lucide-react
npm install axios
npm update
```

---

### **How to Run**

**⚠️ Important:** You will need **two terminals** — one for the backend and one for the frontend.

Also, make sure to create an `.env` file in the **root directory** and include the required API keys (specified in the D2L submission) for privacy.

---

#### **1. Run Backend First:**
```bash
cd server
python app.py
```

---

#### **2. Run Frontend:**
```bash
cd clientfrontend
npm install
npm run build
npm start
```

---

Happy mingling your mood!

