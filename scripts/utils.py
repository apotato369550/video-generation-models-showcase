import os
import json
import time
import uuid
from pathlib import Path
from datetime import datetime
from typing import Tuple

import requests

# Load environment variables
ROOT = Path(__file__).resolve().parent.parent

def _load_env():
    """Load all vars from .env into os.environ, then return KIE_API_KEY."""
    env_path = ROOT / ".env"

    if env_path.exists():
        try:
            import dotenv
            dotenv.load_dotenv(env_path, override=False)
        except ImportError:
            # Fallback: manual parse
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"\'')
                    os.environ.setdefault(key, val)

    api_key = os.environ.get("KIE_API_KEY")
    if not api_key:
        raise RuntimeError("KIE_API_KEY not found in environment or .env file")
    return api_key

KIE_API_KEY = _load_env()

UPLOAD_BASE = "https://kieai.redpandaai.co"
API_BASE = "https://api.kie.ai"
POLL_INTERVAL = 15
POLL_TIMEOUT = 600


def load_inputs() -> Tuple[str, str]:
    """Load image path and prompt text. Respects IMAGE_PATH and PROMPT_FILE env vars."""
    raw_image = os.environ.get("IMAGE_PATH", "data/sample_image.jpeg")
    raw_prompt = os.environ.get("PROMPT_FILE", "data/sample_prompt.txt")

    image_path = str(Path(raw_image) if Path(raw_image).is_absolute() else ROOT / raw_image)
    prompt_path = Path(raw_prompt) if Path(raw_prompt).is_absolute() else ROOT / raw_prompt

    with open(prompt_path, "r") as f:
        prompt_text = f.read()

    print(f"[utils] Loaded image: {image_path}")
    print(f"[utils] Loaded prompt from: {prompt_path}")

    return image_path, prompt_text


def upload_image(image_path: str) -> str:
    """Upload image to KIE and return fileUrl."""
    print(f"[utils] Uploading image: {image_path}")

    with open(image_path, "rb") as f:
        files = {"file": f}
        headers = {"Authorization": f"Bearer {KIE_API_KEY}"}

        response = requests.post(
            f"{UPLOAD_BASE}/api/v1/file/upload/stream",
            files=files,
            headers=headers
        )

    response.raise_for_status()
    data = response.json()

    if not data.get("success"):
        raise RuntimeError(f"Upload failed: {data}")

    file_url = data["data"]["fileUrl"]
    print(f"[utils] Upload successful: {file_url}")
    return file_url


def get_task_detail(task_id: str) -> dict:
    """Fetch task details from API."""
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{API_BASE}/api/v1/jobs/getTaskDetail",
        params={"taskId": task_id},
        headers=headers
    )

    response.raise_for_status()
    return response.json()


def poll_until_done(task_id: str) -> str:
    """Poll task until completion, return video URL."""
    print(f"[utils] Starting poll for task {task_id}")
    start_time = time.time()

    while time.time() - start_time < POLL_TIMEOUT:
        data = get_task_detail(task_id)
        status = data.get("data", {}).get("status")

        print(f"[utils] Task {task_id} status: {status}")

        if status == "succeed":
            task_data = data.get("data", {})

            # Try multiple paths for video URL
            video_url = (
                task_data.get("output", {}).get("videoUrl") or
                task_data.get("output", {}).get("video_url") or
                task_data.get("output", {}).get("url") or
                None
            )

            # Fallback to works array
            if not video_url and task_data.get("works"):
                works = task_data.get("works", [])
                if works:
                    video_url = works[0].get("url") or works[0].get("videoUrl")

            if video_url:
                print(f"[utils] Task succeeded. Video URL: {video_url}")
                return video_url
            else:
                raise RuntimeError(f"Task succeeded but no video URL found in response: {task_data}")

        elif status in ("failed", "error"):
            raise RuntimeError(f"Task failed with status '{status}': {data}")

        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"Task {task_id} did not complete within {POLL_TIMEOUT} seconds")


def run_task(model_name: str, payload: dict, endpoint: str = "/api/v1/jobs/createTask") -> str:
    """Create and run a task, poll until completion, return video URL."""
    print(f"[utils] Running task for model: {model_name}")
    print(f"[utils] Endpoint: {endpoint}")

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{API_BASE}{endpoint}",
        json=payload,
        headers=headers
    )

    response.raise_for_status()
    body = response.json()

    if body.get("code") != 200:
        raise RuntimeError(f"Task creation failed: {body}")

    task_id = body["data"]["taskId"]
    print(f"[utils] Task created with ID: {task_id}")

    video_url = poll_until_done(task_id)
    return video_url


def download_video(url: str, dest_path: str) -> None:
    """Download video from URL to destination path."""
    print(f"[utils] Downloading video from: {url}")
    print(f"[utils] Saving to: {dest_path}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"[utils] Download complete: {dest_path}")


def output_path(provider: str, model_name: str) -> str:
    """Generate output file path with timestamp and UUID."""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{model_name}_{timestamp}_{unique_id}.mp4"

    output_dir = ROOT / "results" / provider
    output_dir.mkdir(parents=True, exist_ok=True)

    path = str(output_dir / filename)
    print(f"[utils] Output path: {path}")
    return path
