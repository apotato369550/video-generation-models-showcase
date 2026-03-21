import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "kling"

MODELS = {
    "kling_3_0": {
        "model": "kling-3.0/video",
        "input": {
            "duration": "10",
            "mode": "pro",
            "aspect_ratio": "16:9",
            "sound": False,
            "multi_shots": False
        }
    },
    "kling_2_6": {
        "model": "kling-2.6/image-to-video",
        "input": {
            "duration": "10",
            "aspect_ratio": "16:9",
            "cfg_scale": 0.5
        }
    },
    "kling_2_1_master": {
        "model": "kling/v2-1-master-image-to-video",
        "input": {
            "cfg_scale": 0.5
        }
    },
    "kling_2_1_pro": {
        "model": "kling/v2-1-pro",
        "input": {
            "duration": "10",
            "cfg_scale": 0.5
        }
    },
    "kling_2_1_standard": {
        "model": "kling/v2-1-standard",
        "input": {
            "duration": "10",
            "cfg_scale": 0.5
        }
    }
}

FLAGSHIP = "kling_3_0"

def run_model(key: str = FLAGSHIP) -> str:
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH)
    cfg = MODELS[key]
    input_params = {**cfg["input"], "prompt": PROMPT}
    if key in ("kling_3_0", "kling_2_6"):
        input_params["image_urls"] = [image_url]
    else:
        input_params["image_url"] = image_url
    payload = {"model": cfg["model"], "input": input_params}
    video_url = utils.run_task(key, payload)
    dest = utils.output_path(PROVIDER, key)
    utils.download_video(video_url, dest)
    print(f"[{PROVIDER}/{key}] saved → {dest}")
    return dest

if __name__ == "__main__":
    import sys as _sys
    target = _sys.argv[1] if len(_sys.argv) > 1 else FLAGSHIP
    if target == "all":
        for k in MODELS:
            run_model(k)
    elif target in MODELS:
        run_model(target)
    else:
        print(f"Unknown model: {target}")
        print("Available:", list(MODELS.keys()))
        _sys.exit(1)
