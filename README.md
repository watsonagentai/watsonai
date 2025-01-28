# WatsonAI 🔎  
[![GitHub stars](https://img.shields.io/github/stars/sherlock-project/sherlock?style=social)](https://github.com/sherlock-project/sherlock/stargazers)
[![Discord](https://img.shields.io/discord/12345.svg?label=Sherlock+Discord)](https://discord.gg/sherlock)
[![Twitter Follow](https://img.shields.io/twitter/follow/sherlockproj?style=social)](https://twitter.com/sherlockproj)

**Watson** is a Dockerized Python application that leverages the [Sherlock](https://github.com/sherlock-project/sherlock) engine to locate user accounts across numerous sites, categorize them, and generate an AI-driven profile summary. Sherlock’s partial output is streamed live (in color), providing real-time feedback during scanning.

---

## Features
- **Single Docker Image** – No separate containers; everything (including a Python venv) is bundled in one build.  
- **Real-Time Sherlock Logs** – Partial line-by-line output with ANSI color.  
- **Categorization** – Discovered sites are mapped to categories (e.g., music, travel, social).  
- **OpenAI Summaries** – Summaries of user interests, grouped categories, and additional insights.

---

## Quick Start

1. **Clone or Download** this repo.  
2. **Create/Update** a `.env` file (for OpenAI key, etc.):
   ```bash
   OPENAI_API_KEY=sk-xxxxxx
   ```
3. **Build** the Docker image:
   ```bash
   docker compose build
   ```
4. **Run** Watson:
   ```bash
   docker compose run watson username123
   ```
   - Partial Sherlock output appears in real time.
   - A final AI summary is generated at the end.

*(If you omit a username, Watson falls back to `SHERLOCK_USERNAME` in `.env`.)*

---

## Usage

- **Multiple Usernames**  
  Pass multiple arguments to process them in one run:
  ```bash
  docker compose run watson user1 user2 user3
  ```
- **Local Execution (Optional)**  
  If not using Docker, install dependencies locally:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python src/main.py user123
  ```
- **OpenAI**  
  The code uses [the new `OpenAI` class](https://pypi.org/project/openai/) (≥1.0.0). Ensure `OPENAI_API_KEY` is set.

---

## How It Works

1. **Sherlock**  
   - Installed via `pip install sherlock`.  
   - Invoked in unbuffered mode (`python -u -m sherlock`) so partial logs appear live.

2. **Partial Logs**  
   - A `subprocess.Popen` reads each line from Sherlock and logs it in bright cyan.

3. **Categorization**  
   - Found sites are parsed and matched against a mapping (e.g., “Behance” ⇒ `design`, `creative`).

4. **AI Summaries**  
   - The histogram of categories is sent to OpenAI’s large language models.  
   - A structured summary is returned, which may include color codes.

---

## License

Watson’s code is provided under your preferred open-source license (e.g. MIT).  
[Sherlock](https://github.com/sherlock-project/sherlock) is under the [MIT License](https://github.com/sherlock-project/sherlock/blob/master/LICENSE).  

Enjoy using **Watson**! If you find it helpful, consider ⭐ starring the Sherlock project as well.
```