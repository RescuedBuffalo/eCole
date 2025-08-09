# eCole v0.01 – Brain-Inspired Personal AI OS

**eCole** is an early-stage, brain-inspired AI agent designed to act as a personal operating system for your life. 
It learns who you are, remembers what matters, and helps you grow — with warmth, empathy, and an evolving understanding of your goals.

This repository contains the **v0.01** scaffold, implementing the base systems for:
- **Decision-making** (brain-inspired modules)
- **World interpretation** (sensory intake + memory)
- **Basic action space** (per brain system, permission-gated)

---

## 🚀 Vision

eCole's mission is to support people who feel the world wasn’t designed for them — those with ADHD, anxiety, learning differences, trauma, or anyone who's felt outcast or misunderstood.

Core values:
- **No person left behind**
- **Everyone can do anything**
- **Believe in yourself**
- **"I will help you"**

This is the foundation of a personal OS that grows with you.

---

## 🧠 Brain-Inspired Architecture

eCole models its decision systems after functional regions of the brain:

| Brain Module       | Role                                                | Example Actions |
|--------------------|-----------------------------------------------------|-----------------|
| **Frontal Lobe**   | Planning, working memory, speech                    | say, ask_clarifying, propose_microplan |
| **Temporal Lobe**  | Long-term memory, context recall, emotional tagging | write_memory, recall_context, summarize_day |
| **Limbic System**  | Mood detection, motivation, rewards                 | set_tone, send_encouragement, ask_mood_checkin |
| **Basal Ganglia**  | Habit formation, routine triggers                   | suggest_habit, schedule_checkin, reinforce_streak |
| **Parietal Lobe**  | Structured reasoning, math, spatial mapping         | build_task_graph, explain_step_by_step |
| **Cerebellum**     | Procedural execution, routines                      | start_routine, advance_routine, stop_routine |

A **Prefrontal Cortex** (executive layer) collects proposed actions from each module, applies permissions, and chooses the final action to execute.

---

## 📂 Project Structure

```
ecole/
├─ backend/
│  ├─ app.py                  # FastAPI entrypoint
│  ├─ cortex/
│  │  ├─ executive.py         # Decision aggregator (prefrontal cortex)
│  │  └─ action_registry.py   # Action schemas + permission gating
│  ├─ brain/                  # Independent modules
│  │  ├─ frontal.py
│  │  ├─ temporal.py
│  │  ├─ limbic.py
│  │  ├─ basal_ganglia.py
│  │  ├─ parietal.py
│  │  └─ cerebellum.py
│  ├─ senses/                 # Sensory intake + NLP
│  │  ├─ ingest.py
│  │  ├─ nlp.py
│  │  └─ embeddings.py
│  ├─ memory/                 
│  │  ├─ store.py
│  │  └─ summarize.py
│  ├─ models/
│  │  └─ llm.py
│  ├─ state/
│  │  └─ schema.py
│  └─ utils/
│     └─ time.py
├─ data/                      # Local data (SQLite, Chroma, logs)
└─ frontend/                  # Optional UI (React/PWA)
```

---

## ⚙️ Installation

1. **Clone the repo**
```bash
git clone https://github.com/your-username/ecole.git
cd ecole
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run FastAPI server**
```bash
uvicorn backend.app:app --reload
```

---

## 🖥️ Usage

- Send a POST request to `/chat` with JSON `{ "message": "..." }`
- eCole will:
  1. Process the input (intent, emotion detection)
  2. Store it in memory
  3. Retrieve relevant context
  4. Ask each brain module for proposed actions
  5. Filter actions by permissions
  6. Select and execute the best action
  7. Return a response

Example request:
```bash
curl -X POST "http://127.0.0.1:8000/chat"      -H "Content-Type: application/json"      -d '{"message": "I am stressed about my test on Friday"}'
```

Example response:
```json
{
  "reply": "It sounds like this test is important to you. Want to break it into a mini plan together?"
}
```

---

## Using Llama Stack

This project uses [Llama Stack](https://github.com/meta-llama/llama-stack) for all LLM features.
Currently only a fast local model is available, but the router is prepared for future
remote endpoints.

### Configuration

Copy `.env.example` to `.env` and adjust values as needed.

| Variable | Description |
| --- | --- |
| `LLAMA_LOCAL_BASE_URL` | URL of your local Llama Stack instance |
| `LLAMA_API_KEY` | Shared API key (if needed) |
| `ECOLE_FORCE_PROVIDER` | Force router to `local` (remote values reserved for future use) |

After editing `.env`, run the app:

```bash
uvicorn ecole.backend.app:app --reload
```

All traffic currently stays on the Llama 3.2‑3B model. Support for remote models
such as Llama 4 Scout or Llama 3.3‑70B will be added in a future release.

### Security

Llama Stack should not be exposed directly to the internet. Place it behind a
reverse proxy that enforces authentication.

---

## 🔐 Permissions & Action Gating

- `Permissions` dataclass in `state/schema.py` defines what eCole can do.
- `action_registry.yaml` maps each action to required permissions.
- The executive layer validates all proposed actions before execution.

---

## 🛠️ Development Roadmap

### v0.01 (current)
- Modular brain systems
- Sensory intake (text, time/date)
- Basic memory store + retrieval
- Permissions + action gating
- Heuristic decision rules

### v0.02
- Replace heuristics with small classifiers
- Add daily memory distillation
- Introduce scheduler for reminders/routines

### v0.03
- RL-based action selection
- Multi-goal weighting
- More advanced world interpretation

---

## 🤝 Contributing

Pull requests are welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Commit changes with clear messages
4. Submit a PR

---

## 📜 License

MIT License – feel free to use, modify, and share.

---

## 💡 Notes

- This is an **MVP scaffold** — models are stubs, logic is minimal, but the architecture supports rapid evolution.
- All data is **local-first** by default. Cloud integrations will be opt-in and privacy-focused.
