import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import utils

IMAGE_PATH, PROMPT = utils.load_inputs()
image_url = None

PROVIDER = "veo"
FLAGSHIP = "veo_3_1_fast"

MODELS = {
    "veo_3_1_fast": {
        "model": "veo-3.1-fast",
        "aspect_ratio": "16:9",
        "duration": 8,
    },
    "veo_3_1_quality": {
        "model": "veo-3.1-quality",
        "aspect_ratio": "16:9",
        "duration": 8,
    },
}


def run_model(key: str = FLAGSHIP) -> str:
    """Run a Veo model and return the output video path."""
    global image_url
    if image_url is None:
        image_url = utils.upload_image(IMAGE_PATH)

    payload = {
        **MODELS[key],
        "prompt": PROMPT,
        "image_url": image_url,
    }

    video_url = utils.run_task(key, payload, endpoint="/api/v1/veo3/generate")
    dest = utils.output_path(PROVIDER, key)
    utils.download_video(video_url, dest)
    print(f"[{PROVIDER}/{key}] saved → {dest}")
    return dest


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Veo video generation models")
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
