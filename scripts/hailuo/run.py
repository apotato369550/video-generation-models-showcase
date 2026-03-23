import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "hailuo"

MODELS = {
    "hailuo_2_3_pro": {
        "model": "hailuo/2-3-image-to-video-pro",
        "input": {
            "duration": "6",
            "resolution": "768P"
        }
    },
    "hailuo_2_3_standard": {
        "model": "hailuo/2-3-image-to-video-standard",
        "input": {
            "duration": "6",
            "resolution": "768P"
        }
    },
    "hailuo_02_pro": {
        "model": "hailuo/02-image-to-video-pro",
        "input": {
            "prompt_optimizer": True
        }
    },
    "hailuo_02_standard": {
        "model": "hailuo/02-image-to-video-standard",
        "input": {
            "prompt_optimizer": True
        }
    }
}

FLAGSHIP = "hailuo_2_3_pro"

def run_model(key=FLAGSHIP):
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH, utils.PROVIDER_MIN_IMAGE_SIZE.get(PROVIDER, 256))
    cfg = MODELS[key]
    input_params = {**cfg["input"], "image_url": image_url, "prompt": PROMPT}
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
