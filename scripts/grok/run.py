import sys
import uuid
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

INPUT_DIR = None  # set by --input arg
_inputs = None    # lazy cache

def _get_inputs():
    global _inputs
    if _inputs is None:
        _inputs = utils.load_inputs(INPUT_DIR)
    return _inputs

image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "grok"

MODELS = {
    "grok_imagine": {
        "model": "grok-imagine/image-to-video",
        "input": {
            "duration": "6",
            "mode": "normal",
            "resolution": "720p"
        }
    }
}

FLAGSHIP = "grok_imagine"


def run_model(key: str = FLAGSHIP) -> str:
    global image_url
    import time as _time
    start = _time.time()
    run_id = str(uuid.uuid4())[:8]
    IMAGE_PATH, PROMPT = _get_inputs()
    log_data = {
        "id": run_id,
        "date": datetime.now().isoformat(timespec="seconds"),
        "provider": PROVIDER,
        "model": key,
        "input_dir": INPUT_DIR,
        "image_path": IMAGE_PATH,
        "prompt": PROMPT,
        "task_id": None,
        "video_url": None,
        "output_path": None,
        "status": "error",
        "error": None,
        "duration_seconds": None,
    }
    try:
        if image_url is None:
            image_url = utils.upload_image(IMAGE_PATH, utils.PROVIDER_MIN_IMAGE_SIZE.get(PROVIDER, 256))
        input_params = {**MODELS[key]["input"], "image_urls": [image_url], "prompt": PROMPT}
        payload = {"model": MODELS[key]["model"], "input": input_params}
        video_url = utils.run_task(key, payload)
        dest = utils.output_path(PROVIDER, key)
        utils.download_video(video_url, dest)
        log_data.update({
            "video_url": video_url,
            "output_path": dest,
            "status": "success",
        })
        print(f"[{PROVIDER}/{key}] saved → {dest}")
        return dest
    except Exception as e:
        log_data["error"] = str(e)
        raise
    finally:
        log_data["duration_seconds"] = round(_time.time() - start, 1)
        utils.write_log(PROVIDER, key, run_id, log_data)


if __name__ == "__main__":
    import argparse as _argparse
    _parser = _argparse.ArgumentParser()
    _parser.add_argument("model", nargs="?", default=FLAGSHIP)
    _parser.add_argument("--input", dest="input_dir", default=None, help="Directory containing sample_image.jpeg and sample_prompt.txt")
    _args = _parser.parse_args()
    INPUT_DIR = _args.input_dir
    target = _args.model
    if target == "all":
        for k in MODELS:
            run_model(k)
    elif target in MODELS:
        run_model(target)
    else:
        print(f"Unknown model: {target}")
        print("Available:", list(MODELS.keys()))
        import sys as _sys
        _sys.exit(1)
