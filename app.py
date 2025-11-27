import streamlit as st
import requests
import json
import re

# =======================
# EURI API CONFIGURATION
# =======================
EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
EURI_API_KEY = "" # Replace with your api key
MODEL = "groq/compound"
MAX_TOKENS = 1024

# =======================
# MINIMAL CSS
# =======================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; }
    h1 { color: #fff !important; text-align: center; font-size: 2.8rem !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); }
    .subtitle { text-align: center; color: #fff; font-size: 1.1rem; margin-bottom: 2rem; }
    .content-card { background: #fff; border-radius: 24px; padding: 2.5rem; box-shadow: 0 20px 60px rgba(0,0,0,0.3); margin: 1rem auto; max-width: 850px; }
    .stRadio > label, .stTextArea > label { font-size: 1rem; font-weight: 600; color: #1a202c; }
    .stRadio > div { background: #f7fafc; padding: 0.8rem; border-radius: 12px; }
    .stRadio > div > label { background: #fff; padding: 0.7rem 1.8rem; border-radius: 10px; margin: 0 0.4rem; border: 2px solid #e2e8f0; transition: all 0.3s; }
    .stRadio > div > label:hover { background: #667eea; color: #fff; border-color: #667eea; transform: translateY(-2px); }
    .stTextArea textarea { border: 2px solid #e2e8f0; border-radius: 12px; padding: 1rem; background: #f7fafc; color: #1a202c; }
    .stTextArea textarea::placeholder { color: #a0aec0; }
    .stTextArea textarea:focus { border-color: #667eea; background: #fff; }
    .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border: none; border-radius: 12px; padding: 0.9rem; font-size: 1.05rem; font-weight: 600; width: 100%; margin-top: 1rem; box-shadow: 0 8px 20px rgba(102,126,234,0.35); transition: all 0.3s; }
    .stButton > button:hover { transform: translateY(-2px); }
    .result-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 2rem; margin: 2rem 0; box-shadow: 0 12px 35px rgba(102,126,234,0.4); }
    .stMetric { background: rgba(0,0,0,0.3); padding: 1.3rem; border-radius: 12px; }
    .stMetric label { color: #fff !important; font-weight: 600 !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
    .stMetric div { color: #fff !important; font-size: 1.9rem !important; font-weight: 700 !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.5); }
    .confidence-box { background: rgba(0,0,0,0.3); padding: 1.3rem; border-radius: 12px; }
    .confidence-label { color: #fff; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.7rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
    .confidence-bar { background: rgba(0,0,0,0.2); border-radius: 8px; height: 28px; overflow: hidden; }
    .confidence-fill { background: linear-gradient(90deg, #48bb78 0%, #38a169 100%); height: 100%; display: flex; align-items: center; justify-content: center; font-weight: 700; transition: width 0.6s; color: #fff; }
    .explanation-box { background: rgba(0,0,0,0.3); border-radius: 12px; padding: 1.5rem; margin-top: 1.5rem; border: 1px solid rgba(255,255,255,0.3); }
    .explanation-title { color: #fff; font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.5); }
    .explanation-text { color: #fff; line-height: 1.8; user-select: text; -webkit-user-select: text; -moz-user-select: text; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }
    .streamlit-expanderHeader { background: rgba(255,255,255,0.2); border-radius: 10px; color: #fff !important; font-weight: 600; }
    .streamlit-expanderContent { background: rgba(255,255,255,0.15); color: #fff; }
    #MainMenu, footer { visibility: hidden; }
    @media (max-width: 768px) { h1 { font-size: 2rem !important; } .content-card { padding: 1.5rem; } }
    </style>
    """, unsafe_allow_html=True)

# =======================
# ANALYSIS FUNCTION
# =======================
def analyze_text(text, mode="sentiment"):
    headers = {"Authorization": f"Bearer {EURI_API_KEY}", "Content-Type": "application/json"}
    system_msg = (
        "You are an expert emotion detection engine. Analyze the text and respond with a JSON like {'label': '<emotion>', 'confidence': <0-100>}, and provide a detailed explanation of why this emotion was detected."
        if mode == "emotion" else
        "You are an expert sentiment analysis engine. Analyze the text and respond with a JSON like {'label': '<positive/negative/neutral>', 'confidence': <0-100>}, and provide a detailed explanation of why this sentiment was detected."
    )
    payload = {"model": MODEL, "max_tokens": MAX_TOKENS, "temperature": 0.2, "messages": [{"role": "system", "content": system_msg}, {"role": "user", "content": text}]}
    try:
        response = requests.post(EURI_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            return {"error": f"API Error {response.status_code}", "details": response.text}
        raw_text = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", raw_text.replace("\n", ""))
        parsed = json.loads(match.group().replace("'", '"')) if match else {}
        return {"parsed": parsed, "explanation": raw_text}
    except Exception as e:
        return {"error": str(e)}

# =======================
# STREAMLIT UI
# =======================
st.set_page_config(page_title="Sentiment & Emotion Analyzer", page_icon="🎯", layout="wide")
load_css()

st.markdown("<h1>🎯 Sentiment & Emotion Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by AI • Analyze text sentiment and emotions instantly</p>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    mode = st.radio("Select Analysis Type:", ["Sentiment", "Emotion"], horizontal=True)
    text_input = st.text_area("Enter your text here:", height=150, placeholder="Type or paste your text here for analysis...")
    
    if st.button("🚀 Analyze Now"):
        if not text_input.strip():
            st.warning("⚠️ Please enter some text to analyze.")
        else:
            with st.spinner(f"🔍 Analyzing {mode}..."):
                result = analyze_text(text_input, mode.lower())
            if "error" in result:
                st.error(f"❌ {result['error']}")
                if "details" in result: st.code(result["details"])
            else:
                parsed = result.get("parsed", {})
                explanation = result.get("explanation", "")
                label = parsed.get("label", "Unknown").capitalize()
                confidence = parsed.get("confidence", 0)
                emoji_map = {"Positive": "😊", "Negative": "😞", "Neutral": "😐", "Joy": "😄", "Sadness": "😢", "Anger": "😠", "Fear": "😨", "Love": "❤️", "Surprise": "😮", "Disgust": "🤢", "Trust": "🤝", "Anticipation": "⏳", "Unknown": "🎯"}
                emoji = emoji_map.get(label, "🎯")
                
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(label=f"{mode} Detected", value=f"{emoji} {label}")
                with col2:
                    st.markdown(f"<div class='confidence-box'><div class='confidence-label'>Confidence Level</div><div class='confidence-bar'><div class='confidence-fill' style='width: {confidence}%;'>{confidence}%</div></div></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='explanation-box'><div class='explanation-title'>💡 Detailed Analysis</div><div class='explanation-text'>{explanation}</div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                with st.expander("🔍 View Raw API Response"):
                    st.json(parsed)
    st.markdown("</div>", unsafe_allow_html=True)
