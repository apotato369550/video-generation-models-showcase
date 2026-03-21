# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo does

Runs image-to-video generation jobs against multiple kie.ai API providers and saves the output clips locally. One image + one prompt → clips from every model across every provider.

## Setup

```bash
pip install -r requirements.txt
# .env must contain KIE_API_KEY, IMAGE_PATH, PROMPT_FILE
```

## Running scripts

```bash
# Single provider, flagship model
python scripts/kling/run.py

# Single provider, specific model
python scripts/kling/run.py kling_2_1_master

# Single provider, all models
python scripts/kling/run.py all

# Batch: all providers
python scripts/generate_batch.py

# Batch: selected providers
python scripts/generate_batch.py --kling --hailuo
```

Available provider flags for `generate_batch.py`: `--kling --bytedance --hailuo --sora --wan --grok --runway`

## Architecture

```
scripts/
  utils.py              # shared: upload, createTask, poll, download, path helpers
  generate_batch.py     # orchestrator: loads providers via importlib, runs all models
  {provider}/run.py     # standalone per-provider script
data/
  sample_image.jpeg     # default input image
  sample_prompt.txt     # default prompt
results/
  {provider}/           # output clips: {model}_{YYYYMMDD}_{uuid8}.mp4
docs/
  {provider}/           # kie.ai OpenAPI specs for each model
```

### utils.py contract

- `load_inputs()` → reads `IMAGE_PATH` / `PROMPT_FILE` env vars (defaults: `data/sample_image.jpeg`, `data/sample_prompt.txt`)
- `upload_image(path)` → POSTs to `https://kieai.redpandaai.co/api/v1/file/upload/stream`, returns `fileUrl`
- `run_task(model_name, payload, endpoint)` → POSTs to `https://api.kie.ai{endpoint}`, polls until done, returns video URL
- `poll_until_done(task_id)` → polls `/api/v1/jobs/getTaskDetail` every 15s, 600s timeout
- `output_path(provider, model_name)` → creates `results/{provider}/` dir, returns timestamped path

Default `endpoint` for `run_task` is `/api/v1/jobs/createTask`. **Runway uses `/api/v1/runway/generate`.**

### Provider script pattern

Every `run.py` follows the same structure:
1. `sys.path.insert(0, parent.parent)` to import `utils` from `scripts/`
2. Module-level `IMAGE_PATH, PROMPT = utils.load_inputs()` and `image_url = None` (lazy upload)
3. `MODELS` dict: `{key: {"model": "<api-model-id>", "input": {<static params>}}}`
4. `FLAGSHIP` string pointing to the default model key
5. `run_model(key)` builds payload, calls `utils.run_task`, downloads result
6. `__main__` block: positional arg = model key, `"all"` runs every model

### Image field variations (provider-specific)

Not all providers use the same field name for the uploaded image URL:

| Provider / Model | Field | Shape |
|---|---|---|
| kling `kling_3_0`, `kling_2_6` | `image_urls` | array `[url]` |
| kling others | `image_url` | string |
| bytedance `seedance_1_5_pro` | `input_urls` | array `[url]` |
| bytedance v1 variants | `image_url` | string |
| hailuo all | `image_url` | string |
| sora all | `image_urls` | array `[url]` |
| wan `wan_2_6` | `image_urls` | array `[url]` |
| wan others | `image_url` | string |
| grok | `image_urls` | array `[url]` |
| runway | `imageUrl` | string (camelCase, top-level — no `input:` wrapper) |

### Runway payload is flat

All providers wrap params in `{"model": "...", "input": {...}}`. **Runway is the exception** — its payload is flat: `{"prompt": ..., "imageUrl": ..., "duration": 5, "quality": "720p", "aspectRatio": "16:9", "waterMark": ""}`.

### generate_batch.py loader

Uses `importlib.util.spec_from_file_location` to load each provider as `{name}_run` to avoid module name collisions. Accesses `mod.MODELS`, `mod.PROVIDER`, `mod.run_model(key)` on each loaded module.

## Adding a new provider

1. Create `scripts/{provider}/run.py` following the pattern above
2. Add `"{provider}"` to `PROVIDERS` in `scripts/generate_batch.py`

## API docs

`docs/{provider}/` contains OpenAPI YAML specs for each model. All standard providers use `POST /api/v1/jobs/createTask`. Task status is always polled via `GET /api/v1/jobs/getTaskDetail?taskId=...`.
