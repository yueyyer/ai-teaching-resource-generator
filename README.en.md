<div align="center">

# AI Teaching Resource Generator

[简体中文](README.md) | **English**

An AI-powered teaching assistant platform for rural education: helps teachers generate lesson plans, quizzes, and multimedia materials in minutes, and provides students with explanations, self-testing, and personalized learning paths.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46-FF4B4B?logo=streamlit&logoColor=white)
![DashScope](https://img.shields.io/badge/LLM-DashScope-FF6A00)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## The Problem It Solves

Rural schools often face teacher shortages and heavy workloads — one teacher may cover multiple subjects, writing lesson plans, exams, and slides from scratch. This system packages LLM capabilities into two workflows:

- **For teachers** — enter a topic and get a structured course outline, PPT content, quiz, case study, or lab guide within minutes, along with AI-generated illustrations and TTS audio, exportable to PDF and saved to the resource library.
- **For students** — knowledge explanations, self-practice with instant feedback, and personalized learning paths visualized as knowledge graphs, giving each student targeted guidance even in large classes.

## Feature Overview

The app uses a teacher / student dual-module design with sidebar switching.

### Teacher Module

| Feature | Description |
|---------|-------------|
| Content Generation | 5 resource types: course outline, teaching PPT, quiz, case study, lab guide; customizable by subject and level |
| Multimodal Input | Speech recognition (iFlytek streaming ASR) and image recognition (OCR) in addition to text |
| Multimedia Studio | Text-to-image generation, TTS (gTTS), iFlytek OCR |
| Resource Management | SQLite-backed library: save, search, categorize, delete; resource link sharing |
| Analytics | Usage statistics and visualization |
| Chat | LLM-powered teaching Q&A assistant |

### Student Module

| Feature | Description |
|---------|-------------|
| Knowledge Explanation | Student-friendly breakdown of concepts |
| Self-Practice | Auto-generated quizzes with instant feedback |
| Personalized Learning | Individual learning paths visualized as knowledge graphs |
| Resource Search | Library retrieval + Wikipedia knowledge augmentation |

### Design Notes

- **Prompt engineering** — each resource type has a dedicated prompt template (`prompts/`) with subject/level parameters injected dynamically; outputs follow a Bloom's-taxonomy-aligned progressive structure.
- **Local persistence** — all generated content is stored in SQLite, searchable and reusable across sessions.
- **Model-agnostic** — LLM calls use the OpenAI-compatible protocol; switch between DashScope / OpenAI / other providers via environment variables.

## Getting Started

### Prerequisites

- Python 3.11+
- An OpenAI-compatible LLM API key (e.g., Alibaba DashScope)
- An iFlytek account (optional — for ASR, OCR, and image generation)

### Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yueyyer/ai-teaching-resource-generator.git
cd ai-teaching-resource-generator

# 2. Install dependencies
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env with your own keys:
#   OpenAI-compatible LLM key (e.g., Alibaba DashScope)
#   iFlytek APPID / APIKEY / APISECRET (for ASR, image generation, OCR)

# 4. Launch
streamlit run exercise.py
```

Open `http://localhost:8501` in your browser.

### Run with Docker

```bash
docker build -t ai-teaching .
docker run -p 8501:8501 --env-file .env ai-teaching
```

## Project Structure

```plaintext
ai-teaching-resource-generator/
├── exercise.py            # Main app entry (teacher/student modules)
├── prompts/               # Prompt templates (outline / PPT / quiz, etc.)
│   ├── tabler_prompt.py   # Course outline generation
│   ├── dictator_prompt.py # Outline structure parsing
│   └── quizzy_prompt.py   # Quiz generation
├── word2picture.py        # Text-to-image API wrapper
├── picture1.py            # Image utilities
├── ocr_scenes_demo.py     # OCR
├── 大模型中文语音识别.py       # iFlytek streaming ASR (Chinese)
├── sidebar_css.py         # Sidebar styles
├── teaching_resources.db  # SQLite resource library
├── requirements.txt
├── Dockerfile
└── .streamlit/config.toml # Streamlit theme
```

> `app.py` is an early English-language prototype (Automated Course Content Generator); the current mainline entry is `exercise.py`.

## Tech Stack

- **UI**: Streamlit with custom CSS (gradient card-based design, themed via `.streamlit/config.toml`)
- **LLM**: OpenAI-compatible SDK, targeting Alibaba DashScope by default
- **Speech**: iFlytek streaming ASR, SpeechRecognition, gTTS
- **Vision**: iFlytek text-to-image, OCR, Pillow
- **Storage**: SQLite (resource library + operation logs)
- **Deployment**: Docker (`python:3.11-slim`)

## Screenshots

> 📌 To be added. Suggested shots:
>
> 1. Teacher "Content Generation" page — input and generated output
> 2. Student "Personalized Learning" knowledge graph
> 3. Resource management page
>
> ```markdown
> ![Content Generation](docs/screenshot-teacher.png)
> ![Knowledge Graph](docs/screenshot-graph.png)
> ```

## Roadmap

- [ ] Direct .pptx export (currently generates outline content)
- [ ] Auto grading and mistake notebook
- [ ] Multi-teacher accounts and class management
- [ ] Offline model support (for schools with limited connectivity)

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
If you find this project useful, a ⭐ star would be appreciated!
</div>
