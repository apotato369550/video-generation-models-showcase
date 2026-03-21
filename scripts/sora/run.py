import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "sora"

MODELS = {
    "sora2": {
        "model": "sora-2-image-to-video",
        "input": {
            "aspect_ratio": "landscape",
            "n_frames": "10",
            "remove_watermark": True,
            "upload_method": "s3"
        }
    },
    "sora2_pro": {
        "model": "sora-2-pro-image-to-video",
        "input": {
            "aspect_ratio": "landscape",
            "n_frames": "15",
            "remove_watermark": True,
            "upload_method": "s3"
        }
    },
    "sora2_characters": {
        "model": "sora-2-characters",
        "input": {
            "aspect_ratio": "landscape",
            "n_frames": "10",
            "remove_watermark": True
        }
    },
    "sora2_characters_pro": {
        "model": "sora-2-characters-pro",
        "input": {
            "aspect_ratio": "landscape",
            "n_frames": "15",
            "remove_watermark": True
        }
    }
}

FLAGSHIP = "sora2_pro"


def run_model(key: str = FLAGSHIP) -> str:
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH)

    payload = MODELS[key].copy()
    payload["input"] = {**MODELS[key]["input"], "prompt": PROMPT, "image_urls": [image_url]}

    video_url = utils.run_task(key, payload)
    dest = utils.output_path(PROVIDER, key)
    utils.download_video(video_url, dest)
    print(f"[{PROVIDER}/{key}] saved → {dest}")
    return dest


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else FLAGSHIP
    if target == "all":
        for k in MODELS:
            run_model(k)
    elif target in MODELS:
        run_model(target)
    else:
        print(f"Unknown model: {target}")
        print("Available:", list(MODELS.keys()))
        sys.exit(1)
