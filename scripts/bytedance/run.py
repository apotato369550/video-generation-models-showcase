import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "bytedance"

MODELS = {
    "seedance_1_5_pro": {
        "model": "bytedance/seedance-1-5-pro",
        "input": {
            "resolution": "1080p",
            "duration": "10"
        }
    },
    "v1_pro": {
        "model": "bytedance/v1-pro-image-to-video",
        "input": {
            "resolution": "720p",
            "duration": "5",
            "camera_fixed": False,
            "seed": -1,
            "enable_safety_checker": True
        }
    },
    "v1_pro_fast": {
        "model": "bytedance/v1-pro-fast-image-to-video",
        "input": {
            "resolution": "720p",
            "duration": "5",
            "camera_fixed": False,
            "seed": -1
        }
    },
    "v1_lite": {
        "model": "bytedance/v1-lite-image-to-video",
        "input": {
            "duration": "5",
            "seed": -1
        }
    }
}

FLAGSHIP = "seedance_1_5_pro"

def run_model(key: str = FLAGSHIP) -> str:
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH)
    payload = MODELS[key].copy()
    payload["input"] = {**MODELS[key]["input"], "image_url": image_url, "prompt": PROMPT}
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
