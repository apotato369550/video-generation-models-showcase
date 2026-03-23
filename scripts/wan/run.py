import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None  # uploaded lazily on first run_model() call

PROVIDER = "wan"

MODELS = {
    "wan_2_6": {
        "model": "wan/2-6-image-to-video",
        "input": {
            "duration": "5",
            "resolution": "1080p"
        }
    },
    "wan_2_6_flash": {
        "model": "wan/2-2-a14b-image-to-video-turbo",
        "input": {
            "resolution": "720p"
        }
    },
    "wan_2_5": {
        "model": "wan/2-5-image-to-video",
        "input": {
            "duration": "5",
            "resolution": "720p"
        }
    },
    "wan_2_2": {
        "model": "wan/2-2-a14b-image-to-video-turbo",
        "input": {
            "resolution": "720p"
        }
    }
}

FLAGSHIP = "wan_2_6"


def run_model(key=FLAGSHIP):
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH, utils.PROVIDER_MIN_IMAGE_SIZE.get(PROVIDER, 256))
    cfg = MODELS[key]
    input_params = {**cfg["input"], "prompt": PROMPT}
    if key == "wan_2_6":
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
