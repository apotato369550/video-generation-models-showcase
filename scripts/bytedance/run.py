import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "bytedance"

MODELS = {
    "seedance_1_5_pro": {
        "model": "bytedance/seedance-1.5-pro",
        "input": {
            "aspect_ratio": "16:9",
            "resolution": "720p",
            "duration": 8,
            "fixed_lens": False,
            "generate_audio": False
        }
    },
    "v1_pro": {
        "model": "bytedance/v1-pro-image-to-video",
        "input": {
            "resolution": "720p",
            "duration": "10"
        }
    },
    "v1_pro_fast": {
        "model": "bytedance/v1-pro-fast-image-to-video",
        "input": {
            "resolution": "720p",
            "duration": "10"
        }
    },
    "v1_lite": {
        "model": "bytedance/v1-lite-image-to-video",
        "input": {
            "resolution": "720p",
            "duration": "10"
        }
    }
}

FLAGSHIP = "seedance_1_5_pro"

def run_model(key: str = FLAGSHIP) -> str:
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH, utils.PROVIDER_MIN_IMAGE_SIZE.get(PROVIDER, 256))
    cfg = MODELS[key]
    input_params = {**cfg["input"], "prompt": PROMPT}
    if key == "seedance_1_5_pro":
        input_params["input_urls"] = [image_url]
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
