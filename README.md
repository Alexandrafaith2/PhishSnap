
# 🐟 PhishSnap – AI-Powered Phishing Triage Tool

PhishSnap is an AI-driven phishing email triage assistant designed for MSPs, SOC teams, helpdesk analysts, and cybersecurity learners. It combines GPT-powered analysis with real-time link extraction and domain intelligence to provide fast, accurate, and actionable phishing insights.

---

## 🚀 Features

- 🧠 AI Phishing Risk Detection using OpenRouter (GPT-based)
- 🔗 Automatic URL extraction from email content
- 🌐 WHOIS lookup for domains (creation date, registrar)
- 🛡 DNS fallback to detect fake or nonexistent domains
- ⚡ **Quick Mode** to skip WHOIS/DNS checks for faster testing
- 📋 Copy/paste-friendly outputs for ticketing, SOC notes, or client responses
- ✅ Local & free to use with open LLMs (no OpenAI account required)

---

## 📸 Preview

> 📥 Paste a suspicious email →  
> 🧠 PhishSnap tells you:
- Is this phishing?
- Why does it look suspicious?
- What should the user do?
- What should IT document?
- Are the links legit?

---

## 📦 Installation

1. **Clone the repo** or download and unzip:
```bash
git clone https://github.com/Alexandrafaith2/phishsnap.git
cd phishsnap
```

2. **Set up a virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** and add your keys:
```env
OPENROUTER_API_KEY=your-openrouter-key
WHOIS_KEY=your-apilayer-key
```

---

## ▶️ Usage

```bash
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) in your browser.

Use Quick Mode for faster response. Disable it for full WHOIS + DNS checks.

---

## 📁 File Structure

```
phishsnap/
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── README.md            # This file
```

---

## ☁️ Deployment (Optional)

Deploy PhishSnap on [Streamlit Cloud](https://streamlit.io/cloud) for free:
- Push code to a public GitHub repo
- Create app in Streamlit Cloud
- Set API keys as **Secrets** in Streamlit settings

---

## 👩‍💻 Built With

- [Streamlit](https://streamlit.io/)
- [OpenRouter.ai](https://openrouter.ai) (GPT-powered analysis)
- [APILayer WHOIS](https://apilayer.com/marketplace/whois-api)
- Python, Regex, DNS & socket lookups

---

## 📬 Contact

Made with 💻 and too much caffeine by Alexandra McKinnon.  
Pull requests and issues welcome!

