import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None

PROVIDER = "runway"
FLAGSHIP = "runway_10s"

MODELS = {
    "runway_10s": {
        "model": "runway-duration-10-generate",
        "duration": 10,
        "quality": "720p",
        "waterMark": "",
    },
    "runway_5s": {
        "model": "runway-duration-5-generate",
        "duration": 5,
        "quality": "1080p",
        "waterMark": "",
    },
}


def run_model(key: str = FLAGSHIP) -> str:
    """Run a Runway model and return the output video path."""
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH)

    payload = {
        **MODELS[key],
        "prompt": PROMPT,
        "imageUrl": image_url,
    }

    video_url = utils.run_task(key, payload, endpoint="/api/v1/runway/generate")
    dest = utils.output_path(PROVIDER, key)
    utils.download_video(video_url, dest)
    print(f"[{PROVIDER}/{key}] saved → {dest}")
    return dest


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Runway video generation models")
    parser.add_argument(
        "--model",
        type=str,
        default=FLAGSHIP,
        choices=list(MODELS.keys()),
        help=f"Model to run (default: {FLAGSHIP})",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all available models sequentially",
    )

    args = parser.parse_args()

    if args.all:
        results = {}
        for model_key in MODELS.keys():
            try:
                results[model_key] = run_model(model_key)
            except Exception as e:
                print(f"[{PROVIDER}/{model_key}] ERROR: {e}")
                results[model_key] = None
        print(f"\n[{PROVIDER}] Results: {results}")
    else:
        run_model(args.model)
