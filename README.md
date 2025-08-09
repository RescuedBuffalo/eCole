# eCole

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
