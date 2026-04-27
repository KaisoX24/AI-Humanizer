# AI Humanizer

A Streamlit-based web application that rewrites AI-generated or overly formal text into more natural, human-like writing. It focuses on reducing detectable AI patterns by introducing variation, imperfection, and realistic tone control.

---

## Features:

* 📄 **File Upload Support**

  * Upload `.txt` or `.pdf` files
  * Automatic text extraction from PDFs

* 🎭 **Tone Control**

  * **Casual** → relaxed, conversational writing
  * **Academic** → structured but human-like scholarly tone

* 🎚️ **Humanization Intensity**

  * **Light** → minimal changes, keeps structure intact
  * **Medium** → moderate rewriting and variation
  * **Heavy** → aggressive rewriting with strong human-like variation

* 🔁 **Multi-pass Refinement**

  * Heavy mode applies a second pass to further reduce AI patterns

* 💾 **Download Output**

  * Export the humanized content instantly

---

## How It Works:

The system uses a combination of:

* Prompt engineering with strict human-writing rules
* Tone and intensity mapping
* Controlled randomness via temperature
* Structural rewriting (sentence variation, contractions, filler phrases)

The goal is to transform text so it:

* Feels natural and less robotic
* Avoids common AI writing patterns
* Mimics real human imperfections

---

## Tech Stack

* **Frontend/UI**: Streamlit
* **LLM API**: Groq (`openai/gpt-oss-20b`)
* **PDF Processing**: PyPDF2
* **Environment Management**: python-dotenv

---

## 📂 Project Structure

```
AI-Humanizer/
│
├── main.py                  # Streamlit app entry point
├── modules/
│   ├── humanizer.py        # Core rewriting logic
│   ├── sys_prompt.py       # Humanization rules prompt
│   ├── text_extractor.py   # PDF text extraction
│
├── .env                    # API keys (not included)
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/KaisoX24/ai-humanizer.git
cd ai-humanizer
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## Running the App

```bash
streamlit run main.py
```

---

## Contributing

Contributions are welcome!
Feel free to open issues or submit pull requests.

---

## 📄 License

This project is licensed under the MIT License.

---
