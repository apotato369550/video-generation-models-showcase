import os
import json
import time
import uuid
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Tuple

import requests
from PIL import Image

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

API_BASE = "https://api.kie.ai"
UPLOAD_BASE = "https://kieai.redpandaai.co"
POLL_INTERVAL = 15
POLL_TIMEOUT = 600

# Minimum image dimension (px) required by each provider.
# Both width and height are scaled up to this if either falls below it.
PROVIDER_MIN_IMAGE_SIZE = {
    "kling":     256,
    "grok":      256,
    "hailuo":    300,
    "bytedance": 256,  # unconfirmed — update if rejected
    "wan":       256,  # unconfirmed — update if rejected
    "sora":      256,  # unconfirmed — update if rejected
    "runway":    256,  # unconfirmed — update if rejected
}


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


def upload_image(image_path: str, min_size: int = 256) -> str:
    """Upload image to KIE and return fileUrl. Resizes if either dimension < min_size px."""
    print(f"[utils] Uploading image: {image_path}")

    # Check and resize if necessary
    img = Image.open(image_path)
    width, height = img.size
    print(f"[utils] Image dimensions: {width}x{height}")

    upload_path = image_path
    temp_file = None

    if width < min_size or height < min_size:
        print(f"[utils] Image too small (min {min_size}px required). Resizing...")
        # Scale up the short side to min_size, preserve aspect ratio
        scale = max(min_size / width, min_size / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        temp_path = temp_file.name
        temp_file.close()
        img_resized.save(temp_path, quality=95)
        upload_path = temp_path
        print(f"[utils] Resized to {new_width}x{new_height}, saved to temp file: {upload_path}")

    try:
        with open(upload_path, "rb") as f:
            files = {"file": f}
            data = {"uploadPath": "uploads"}
            headers = {"Authorization": f"Bearer {KIE_API_KEY}"}

            response = requests.post(
                f"{UPLOAD_BASE}/api/file-stream-upload",
                files=files,
                data=data,
                headers=headers
            )

        response.raise_for_status()
        resp_data = response.json()

        if not resp_data.get("success"):
            raise RuntimeError(f"Upload failed: {resp_data}")

        file_url = resp_data["data"].get("downloadUrl") or resp_data["data"].get("fileUrl")
        print(f"[utils] Upload successful: {file_url}")
        return file_url
    finally:
        # Clean up temp file if it was created
        if temp_file:
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"[utils] Warning: failed to delete temp file {temp_path}: {e}")



def poll_until_done(task_id: str, poll_endpoint: str = "/api/v1/jobs/recordInfo") -> str:
    """Poll task until completion, return video URL."""
    print(f"[utils] Starting poll for task {task_id}")
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }
    start_time = time.time()

    while time.time() - start_time < POLL_TIMEOUT:
        response = requests.get(
            f"{API_BASE}{poll_endpoint}",
            params={"taskId": task_id},
            headers=headers
        )
        response.raise_for_status()
        body = response.json()
        task_data = (body.get("data") or {})
        state = task_data.get("state")

        print(f"[utils] Task {task_id} state: {state}")

        if state == "success":
            if poll_endpoint == "/api/v1/runway/record-detail":
                video_url = (task_data.get("videoInfo") or {}).get("videoUrl")
            else:
                result_json = json.loads(task_data.get("resultJson", "{}"))
                video_urls = result_json.get("resultUrls", [])
                video_url = video_urls[0] if video_urls else None

            if not video_url:
                raise RuntimeError(f"Task succeeded but no video URL found: {task_data}")
            print(f"[utils] Task succeeded. Video URL: {video_url}")
            return video_url

        elif state == "fail":
            fail_msg = task_data.get("failMsg", "unknown")
            fail_code = task_data.get("failCode", "N/A")
            raise RuntimeError(f"Task failed [{fail_code}]: {fail_msg}")

        time.sleep(POLL_INTERVAL)

    raise TimeoutError(f"Task {task_id} did not complete within {POLL_TIMEOUT} seconds")


def run_task(model_name: str, payload: dict, endpoint: str = "/api/v1/jobs/createTask", poll_endpoint: str = "/api/v1/jobs/recordInfo") -> str:
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

    video_url = poll_until_done(task_id, poll_endpoint)
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
