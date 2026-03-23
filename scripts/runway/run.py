import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None

PROVIDER = "runway"
FLAGSHIP = "runway_10s"

MODELS = {
    "runway_5s": {
        "duration": 5,
        "quality": "720p",
        "aspectRatio": "16:9",
        "waterMark": ""
    },
    "runway_10s": {
        "duration": 10,
        "quality": "720p",
        "aspectRatio": "16:9",
        "waterMark": ""
    }
}


def run_model(key: str = FLAGSHIP) -> str:
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH, utils.PROVIDER_MIN_IMAGE_SIZE.get(PROVIDER, 256))

    payload = {
        **MODELS[key],
        "prompt": PROMPT,
        "imageUrl": image_url,
    }

    video_url = utils.run_task(key, payload, endpoint="/api/v1/runway/generate", poll_endpoint="/api/v1/runway/record-detail")
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
