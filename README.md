
# 🎯 Sentiment & Emotion Analyzer

A application that analyzes text sentiment and emotions using AI-powered analysis through the EURI API.


## 📋 Overview

This application uses advanced AI models to analyze text and detect:
- **Sentiment Analysis**: Positive, Negative, or Neutral
- **Emotion Detection**: Joy, Sadness, Anger, Fear, Love, Surprise, and more

## ✨ Features

- 🎨 Beautiful modern UI
- 🤖 Powered by Groq Compound AI model
- 📊 Confidence score visualization
- 💡 Detailed analysis explanations
- 📱 Responsive design for all devices
- ⚡ Real-time analysis

## 🚀 Demo

Simply enter your text, select analysis type (Sentiment or Emotion), and click "Analyze Now" to get instant results with confidence scores and detailed explanations.

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentiment-emotion-analyzer.git
cd sentiment-emotion-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
The app will automatically open at `http://localhost:8501`

## 📦 Dependencies

Create a `requirements.txt` file with:
```
streamlit>=1.28.0
requests>=2.31.0
```

## 🔑 API Configuration

The app uses the EURI API for AI-powered analysis. MODEL = "groq/compound. in your can use any model/platfrom which is suitable for you.

## 📖 Usage

1. **Select Analysis Type**: Choose between "Sentiment" or "Emotion"
2. **Enter Text**: Type or paste your text in the text area
3. **Analyze**: Click the "🚀 Analyze Now" button
4. **View Results**: Get instant results with:
   - Detected sentiment/emotion with emoji
   - Confidence percentage
   - Detailed AI explanation
   - Raw API response (expandable)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [EURI API](https://euron.one/)
- EURI AI Model: Groq Compound

### `requirements.txt`
```
streamlit>=1.28.0
requests>=2.31.0
