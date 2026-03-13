# 🌈 Prism — AI Agent Router System

Prism is an intelligent automation system that reads your notes from **Google Drive**, uses the **Groq API (LLaMA 3.3-70B)** to route your questions to the most suitable AI agent, and then automatically types those prompts into **Claude, ChatGPT, Perplexity, and Gemini** — all inside Chrome.

---

## ✨ Features

- 🧠 **Smart AI Routing** — Groq (LLaMA 3.3-70B) reads your notes and decides which AI agent(s) should answer
- 🔗 **Interdependent Prompts** — All agents receive related, cross-referencing prompts on the same topic for 360° coverage
- 🤖 **4 Specialized Agents**:
  | Agent | Best At |
  |---|---|
  | **Claude** | Coding, debugging, technical implementation |
  | **ChatGPT** | Concepts, learning, creative writing |
  | **Perplexity** | Research, real-world data, citations |
  | **Gemini** | Synthesis, data analysis, summaries |
- ☁️ **Google Drive Integration** — Reads `notes.txt` directly from your Drive
- 💾 **Response Capture** — Saves all AI responses to `ai_responses.json`

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/prism_mac.git
cd prism_mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the example env template and fill in your API key:
```bash
cp .env.example .env
```
Open `.env` and replace the placeholder with your real **Groq API key**:
```
GROQ_API_KEY=your_actual_key_here
```
Get your key at 👉 [https://console.groq.com/keys](https://console.groq.com/keys)

### 4. Set Up Google Drive API
1. Go to [Google Cloud Console](https://console.cloud.google.com/) and create a project
2. Enable the **Google Drive API**
3. Download your OAuth 2.0 credentials as `client_secret_2.json` and place it in the project folder
4. Run the script once — it will open a browser to authenticate and save `credentials.json`

> ⚠️ **Important**: `credentials.json` and `client_secret_2.json` are in `.gitignore` and should **never** be committed.

### 5. Create Your Notes File in Google Drive
Create a file named **`notes.txt`** in the root of your Google Drive with your questions/topics.

---

## 🏃 Usage

```bash
python prism.py
```

Prism will:
1. Check Google Drive for **new or changed** content in `notes.txt`
2. Send the notes to **Groq** for AI-powered routing
3. Launch **Chrome** and open each assigned AI agent in a new tab
4. Automatically type and submit the interdependent prompts
5. Collect and save responses to `ai_responses.json`

---

## 📁 Project Structure

```
prism_mac/
├── prism.py              # Main script
├── requirements.txt      # Python dependencies
├── .env                  # API Keys (not committed)
├── .gitignore
├── settings.yaml         # Google OAuth settings
├── credentials.json      # Google credentials (not committed)
├── client_secret_2.json  # Google client secret (not committed)
├── prev_notes.txt        # Cached last-seen notes (runtime file)
└── ai_responses.json     # Saved AI responses (runtime file)
```

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

---

## 🔒 Security Note

> **Never commit your `.env`, `credentials.json`, or `client_secret_2.json` files.**
> These contain sensitive credentials. They are excluded via `.gitignore`.

---

## 🛠️ Requirements

- Python 3.9+
- Google Chrome installed
- A Google account with Drive access
- A Groq API account (free tier available)

---

## 📜 License

MIT License — free to use and modify.
