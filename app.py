
# app.py – PhishSnap AI (Fast Mode w/ Quick Toggle, WHOIS skip, Faster LLM)
import streamlit as st
import requests
import os
import re
import socket
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
WHOIS_KEY = os.getenv("WHOIS_KEY")

st.set_page_config(page_title="PhishSnap AI", page_icon="🐟")
st.title("📧 PhishSnap – AI Phishing Triage Assistant")

st.markdown("""
Paste a suspicious email below and let AI analyze it for phishing.
PhishSnap now runs in **Fast Mode** with:
- ⏱️ Reduced response time
- 🧠 Lighter LLM (Mistral)
- 🧪 Optional WHOIS + DNS lookup
""")

quick_mode = st.checkbox("🚀 Enable Quick Mode (skip WHOIS + DNS for speed)", value=True)

email_input = st.text_area("📥 Paste suspicious email content here:", height=250)

def extract_links(text):
    return re.findall(r'(https?://[^\s]+)', text)

def extract_domains(text):
    urls = extract_links(text)
    domains = [re.sub(r'^www\.', '', re.findall(r'https?://([^/]+)', url)[0]) for url in urls]
    return list(set(domains))

def get_whois_data(domain):
    try:
        url = f"https://api.apilayer.com/whois/query?domain={domain}"
        headers = {"apikey": WHOIS_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "WHOIS: Domain not found or info unavailable."}
        else:
            return {"error": f"WHOIS error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def domain_exists_dns(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

if st.button("🧠 Analyze Email"):
    if not email_input.strip():
        st.warning("Please paste an email to analyze.")
    else:
        with st.spinner("Analyzing with AI..."):
            prompt = f"""
You are a cybersecurity analyst assistant trained to identify phishing emails.
Analyze the following email and respond with a JSON object containing:
1. risk_level: Low / Medium / High
2. indicators: List of key phishing signs (e.g., spoofed domain, suspicious links)
3. explanation: Plain English reason why this is or isn’t phishing
4. user_response: Message to send back to user who reported it
5. internal_summary: One-paragraph summary for IT or SOC team

Email to analyze:
---
{email_input}
---
"""
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "HTTP-Referer": "https://phishsnap.streamlit.app/",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "mistralai/mistral-7b-instruct",
                        "messages": [
                            {"role": "system", "content": "You are a helpful AI trained in phishing detection."},
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()
                    ai_reply = result['choices'][0]['message']['content']
                    st.subheader("📊 AI Phishing Analysis")
                    st.code(ai_reply, language="json")
                else:
                    st.error(f"AI Error: {response.status_code} – {response.text}")
            except Exception as e:
                st.error(f"AI Error: {e}")

        # Extract and show URLs
        st.subheader("🔗 Extracted URLs")
        urls = extract_links(email_input)
        if urls:
            for link in urls:
                st.markdown(f"- {link}")
        else:
            st.info("No links found in the email.")

        # WHOIS info with DNS fallback (if not in quick mode)
        if not quick_mode:
            st.subheader("🌐 Domain WHOIS Info (with DNS Fallback)")
            domains = extract_domains(email_input)
            if domains:
                for domain in domains:
                    whois = get_whois_data(domain)
                    st.markdown(f"**{domain}**")
                    if "error" in whois:
                        st.warning(whois["error"])
                        if domain_exists_dns(domain):
                            st.success("✅ Domain exists (via DNS), but WHOIS info is unavailable or private.")
                        else:
                            st.error("❌ Domain does not resolve (DNS check failed). Likely fake.")
                    else:
                        st.write(f"- Registrar: {whois.get('registrar_name', 'N/A')}")
                        st.write(f"- Created On: {whois.get('created_date', 'N/A')}")
                        st.write(f"- Updated On: {whois.get('updated_date', 'N/A')}")
            else:
                st.info("No domains to check.")
