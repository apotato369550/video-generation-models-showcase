"""
kie.ai — Image-to-Video API Reference Snippets
================================================
All models that accept an image input on kie.ai, as of March 2026.

Assumes:
  - KIE_API_KEY is set in your environment
  - reference_image.png (or .jpg) is in the current working directory
  - No callback server — uses polling via get_task_details()

Docs: https://docs.kie.ai
Upload API: https://kieai.redpandaai.co
Generation API: https://api.kie.ai

Flow for every model:
  1. upload_image()  →  returns a publicly accessible image URL
  2. create_task()   →  returns a taskId
  3. poll_task()     →  returns the final video URL when done
"""

import os
import time
import requests

# ── Config ────────────────────────────────────────────────────────────────────
KIE_API_KEY    = os.environ["KIE_API_KEY"]
IMAGE_PATH     = "reference_image.png"   # swap to .jpg if needed
PROMPT         = "A person walks slowly through a misty forest at dawn, cinematic wide shot, warm golden light filtering through the trees, slow camera push forward"

HEADERS        = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}
UPLOAD_BASE    = "https://kieai.redpandaai.co"
API_BASE       = "https://api.kie.ai"
POLL_INTERVAL  = 15   # seconds between status checks
POLL_TIMEOUT   = 600  # 10 minutes max wait


# ── Shared helpers ─────────────────────────────────────────────────────────────

def upload_image(image_path: str) -> str:
    """
    Upload a local image via File Stream Upload.
    Returns the public fileUrl string.
    Uploaded files expire after 3 days.
    """
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{UPLOAD_BASE}/api/v1/file/upload/stream",
            headers={"Authorization": f"Bearer {KIE_API_KEY}"},
            files={"file": (os.path.basename(image_path), f)},
        )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"Upload failed: {data}")
    url = data["data"]["fileUrl"]
    print(f"[upload] {url}")
    return url


def get_task_details(task_id: str) -> dict:
    """Poll the unified task status endpoint."""
    resp = requests.get(
        f"{API_BASE}/api/v1/jobs/getTaskDetail",
        headers=HEADERS,
        params={"taskId": task_id},
    )
    resp.raise_for_status()
    return resp.json()


def poll_until_done(task_id: str) -> str:
    """
    Poll every POLL_INTERVAL seconds until the task succeeds or fails.
    Returns the video URL on success.
    Terminal statuses: succeed / failed / error
    """
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        result = get_task_details(task_id)
        status = result.get("data", {}).get("status", "")
        print(f"[{task_id}] status: {status}")
        if status == "succeed":
            # video URL lives at data.output.videoUrl or data.works[0].url
            # — exact path varies by model; walk the response to find it
            output = result["data"].get("output") or {}
            video_url = (
                output.get("videoUrl")
                or output.get("video_url")
                or output.get("url")
            )
            if not video_url:
                # fallback: some models nest it under works[]
                works = result["data"].get("works", [])
                if works:
                    video_url = works[0].get("url") or works[0].get("videoUrl")
            print(f"[{task_id}] done → {video_url}")
            return video_url
        elif status in ("failed", "error"):
            raise RuntimeError(f"Task failed: {result}")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"Task {task_id} did not complete within {POLL_TIMEOUT}s")


def run(model_name: str, payload: dict) -> str:
    """Submit a createTask request and poll to completion."""
    resp = requests.post(
        f"{API_BASE}/api/v1/jobs/createTask",
        headers=HEADERS,
        json=payload,
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("code") != 200:
        raise RuntimeError(f"[{model_name}] createTask error: {body}")
    task_id = body["data"]["taskId"]
    print(f"[{model_name}] taskId: {task_id}")
    return poll_until_done(task_id)


# ── Step 0: Upload once, reuse URL everywhere ──────────────────────────────────
image_url = upload_image(IMAGE_PATH)


# ══════════════════════════════════════════════════════════════════════════════
# KLING
# ══════════════════════════════════════════════════════════════════════════════

def kling_2_6_i2v():
    """Kling 2.6 Image to Video — latest standard tier, 5 or 10s, 720p/1080p"""
    return run("kling/2.6 i2v", {
        "model": "kling/v2-6-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "10",           # "5" or "10"
            "aspect_ratio": "16:9",
            "cfg_scale": 0.5,
            "negative_prompt": "blur, distortion, watermark",
        },
    })


def kling_2_5_turbo_i2v():
    """Kling 2.5 Turbo Pro Image to Video — faster, multi-step prompt parsing"""
    return run("kling/2.5-turbo i2v", {
        "model": "kling/v2-5-turbo-image-to-video-pro",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "10",
            "cfg_scale": 0.5,
        },
    })


def kling_2_1_master_i2v():
    """Kling 2.1 Master — hyper-realistic 1080p, premium tier, 5s only"""
    return run("kling/2.1-master i2v", {
        "model": "kling/v2-1-master-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            # Master only supports 5s
            "cfg_scale": 0.5,
        },
    })


def kling_2_1_pro_i2v():
    """Kling 2.1 Pro — 1080p, 5 or 10s"""
    return run("kling/2.1-pro i2v", {
        "model": "kling/v2-1-pro-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "10",
            "cfg_scale": 0.5,
        },
    })


def kling_2_1_standard_i2v():
    """Kling 2.1 Standard — 720p, cheapest Kling tier, 5 or 10s"""
    return run("kling/2.1-standard i2v", {
        "model": "kling/v2-1-standard-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "10",
            "cfg_scale": 0.5,
        },
    })


def kling_3_0_i2v():
    """Kling 3.0 — latest gen, highest quality, image-to-video"""
    return run("kling/3.0 i2v", {
        "model": "kling/v3-0-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "10",
            "cfg_scale": 0.5,
        },
    })


# ══════════════════════════════════════════════════════════════════════════════
# BYTEDANCE (Seedance / PixelDance)
# ══════════════════════════════════════════════════════════════════════════════

def bytedance_v1_pro_i2v():
    """Bytedance V1 Pro Image to Video — 720p/1080p, 5–8s, camera_fixed control"""
    return run("bytedance/v1-pro i2v", {
        "model": "bytedance/v1-pro-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "resolution": "720p",       # "720p" or "1080p"
            "duration": "5",            # "5" or "8"
            "camera_fixed": False,      # True = locked camera, False = free movement
            "seed": -1,                 # -1 = random
            "enable_safety_checker": True,
        },
    })


def bytedance_v1_pro_fast_i2v():
    """Bytedance V1 Pro Fast — same as Pro but faster inference"""
    return run("bytedance/v1-pro-fast i2v", {
        "model": "bytedance/v1-pro-fast-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "resolution": "720p",
            "duration": "5",
            "camera_fixed": False,
            "seed": -1,
        },
    })


def bytedance_v1_lite_i2v():
    """Bytedance V1 Lite — budget tier, lower res"""
    return run("bytedance/v1-lite i2v", {
        "model": "bytedance/v1-lite-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "5",
            "seed": -1,
        },
    })


def bytedance_seedance_1_5_pro():
    """Bytedance Seedance 1.5 Pro — latest ByteDance model, multi-shot capable"""
    return run("bytedance/seedance-1.5-pro i2v", {
        "model": "bytedance/seedance-1-5-pro",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "resolution": "1080p",
            "duration": "10",
        },
    })


# ══════════════════════════════════════════════════════════════════════════════
# HAILUO (MiniMax)
# ══════════════════════════════════════════════════════════════════════════════

def hailuo_2_3_pro_i2v():
    """Hailuo 2.3 Pro Image to Video — highest quality MiniMax model, 6–10s"""
    return run("hailuo/2.3-pro i2v", {
        "model": "hailuo/2-3-image-to-video-pro",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "6",            # "6" or "10"
            "resolution": "768P",       # "768P" or "1080P"
        },
    })


def hailuo_2_3_standard_i2v():
    """Hailuo 2.3 Standard Image to Video — cheaper than Pro"""
    return run("hailuo/2.3-standard i2v", {
        "model": "hailuo/2-3-image-to-video-standard",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "6",
            "resolution": "768P",
        },
    })


def hailuo_02_pro_i2v():
    """Hailuo 02 Pro Image to Video — previous gen Pro"""
    return run("hailuo/02-pro i2v", {
        "model": "hailuo/02-image-to-video-pro",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "6",
        },
    })


def hailuo_02_standard_i2v():
    """Hailuo 02 Standard Image to Video — previous gen Standard"""
    return run("hailuo/02-standard i2v", {
        "model": "hailuo/02-image-to-video-standard",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": "6",
        },
    })


# ══════════════════════════════════════════════════════════════════════════════
# SORA 2 (OpenAI, via kie.ai)
# ══════════════════════════════════════════════════════════════════════════════

def sora2_i2v():
    """Sora 2 Standard Image to Video — 10s, 720p"""
    return run("sora2 i2v", {
        "model": "sora-2-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],  # note: array, not single string
            "aspect_ratio": "landscape",  # "landscape" | "portrait" | "square"
            "n_frames": "10",           # maps to ~10 seconds
            "remove_watermark": True,
            "upload_method": "s3",
        },
    })


def sora2_pro_i2v():
    """Sora 2 Pro Image to Video — 10–15s, 720p, higher quality"""
    return run("sora2-pro i2v", {
        "model": "sora-2-pro-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],
            "aspect_ratio": "landscape",
            "n_frames": "15",           # "10" or "15"
            "remove_watermark": True,
            "upload_method": "s3",
        },
    })


def sora2_characters_i2v():
    """
    Sora 2 Characters — persistent character from a reference image.
    Your uploaded image IS the character reference.
    This is the equivalent of Cameo via the kie.ai pipeline.
    """
    return run("sora2-characters i2v", {
        "model": "sora-2-characters",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],  # character reference image
            "aspect_ratio": "landscape",
            "n_frames": "10",
            "remove_watermark": True,
        },
    })


def sora2_characters_pro_i2v():
    """Sora 2 Characters Pro — same as Characters but higher quality output"""
    return run("sora2-characters-pro i2v", {
        "model": "sora-2-characters-pro",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],
            "aspect_ratio": "landscape",
            "n_frames": "15",
            "remove_watermark": True,
        },
    })


# ══════════════════════════════════════════════════════════════════════════════
# WAN (Alibaba)
# ══════════════════════════════════════════════════════════════════════════════

def wan_2_6_i2v():
    """Wan 2.6 Image to Video — multi-shot, native audio, up to 15s, 1080p"""
    return run("wan/2.6 i2v", {
        "model": "wan/2-6-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],  # array
            "duration": "10",           # "5" or "10" or "15"
            "resolution": "1080p",      # "480p" | "720p" | "1080p"
        },
    })


def wan_2_6_flash_i2v():
    """Wan 2.6 Flash Image to Video — faster, cheaper variant of 2.6"""
    return run("wan/2.6-flash i2v", {
        "model": "wan/2-6-flash-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],
            "duration": "5",
            "resolution": "720p",
        },
    })


def wan_2_5_i2v():
    """Wan 2.5 Image to Video — previous gen, still solid"""
    return run("wan/2.5 i2v", {
        "model": "wan/2-5-image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],
            "duration": "5",
            "resolution": "720p",
        },
    })


def wan_2_2_i2v():
    """Wan 2.2 A14B Image to Video Turbo — older/faster/cheapest Wan tier"""
    return run("wan/2.2 i2v turbo", {
        "model": "wan/2-2-a14b-image-to-video-turbo",
        "input": {
            "prompt": PROMPT,
            "image_urls": [image_url],
            "duration": "5",
        },
    })


# ══════════════════════════════════════════════════════════════════════════════
# VEO 3.1 (Google, via dedicated kie.ai Veo API)
# Note: Veo uses a *different* endpoint structure than the Market models above
# ══════════════════════════════════════════════════════════════════════════════

def veo_3_1_i2v(quality: str = "fast"):
    """
    Veo 3.1 Image to Video via kie.ai's dedicated Veo API.
    quality: "fast" (cheaper) or "quality" (premium)
    Duration: 8s default. Supports first-frame image input.
    """
    resp = requests.post(
        f"{API_BASE}/api/v1/veo3/generate",
        headers=HEADERS,
        json={
            "model": f"veo-3.1-{quality}",   # "veo-3.1-fast" or "veo-3.1-quality"
            "prompt": PROMPT,
            "image_url": image_url,           # used as first frame
            "aspect_ratio": "16:9",
            "duration": 8,                    # seconds
        },
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("code") != 200:
        raise RuntimeError(f"[veo3.1-{quality}] error: {body}")
    task_id = body["data"]["taskId"]
    print(f"[veo3.1-{quality}] taskId: {task_id}")
    return poll_until_done(task_id)


# ══════════════════════════════════════════════════════════════════════════════
# RUNWAY (via kie.ai Runway API)
# Note: Runway also uses its own dedicated endpoint
# ══════════════════════════════════════════════════════════════════════════════

def runway_gen3_i2v(duration: int = 10):
    """
    Runway Gen-3 (or Aleph) Image to Video via kie.ai Runway API.
    duration: 5 or 10. If 10s, resolution is capped at 720p.
    """
    resp = requests.post(
        f"{API_BASE}/api/v1/runway/generate",
        headers=HEADERS,
        json={
            "prompt": PROMPT,
            "imageUrl": image_url,
            "model": f"runway-duration-{duration}-generate",  # e.g. "runway-duration-10-generate"
            "waterMark": "",            # empty string = no watermark
            "duration": duration,
            "quality": "720p" if duration == 10 else "1080p",
        },
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("code") != 200:
        raise RuntimeError(f"[runway gen3] error: {body}")
    task_id = body["data"]["taskId"]
    print(f"[runway] taskId: {task_id}")
    return poll_until_done(task_id)


# ══════════════════════════════════════════════════════════════════════════════
# GROK IMAGINE (xAI, via kie.ai Market)
# ══════════════════════════════════════════════════════════════════════════════

def grok_imagine_i2v():
    """Grok Imagine Image to Video — xAI model, native audio, configurable duration"""
    return run("grok-imagine i2v", {
        "model": "grok-imagine/image-to-video",
        "input": {
            "prompt": PROMPT,
            "image_url": image_url,
            "duration": 10,
            "aspect_ratio": "16:9",
            "resolution": "720p",
        },
    })


# ══════════════════════════════════════════════════════════════════════════════
# RUN ALL / RUN ONE
# ══════════════════════════════════════════════════════════════════════════════

ALL_MODELS = {
    # Kling
    "kling_3_0":           kling_3_0_i2v,
    "kling_2_6":           kling_2_6_i2v,
    "kling_2_5_turbo":     kling_2_5_turbo_i2v,
    "kling_2_1_master":    kling_2_1_master_i2v,
    "kling_2_1_pro":       kling_2_1_pro_i2v,
    "kling_2_1_standard":  kling_2_1_standard_i2v,
    # Bytedance
    "bytedance_seedance_1_5":    bytedance_seedance_1_5_pro,
    "bytedance_v1_pro":          bytedance_v1_pro_i2v,
    "bytedance_v1_pro_fast":     bytedance_v1_pro_fast_i2v,
    "bytedance_v1_lite":         bytedance_v1_lite_i2v,
    # Hailuo
    "hailuo_2_3_pro":      hailuo_2_3_pro_i2v,
    "hailuo_2_3_standard": hailuo_2_3_standard_i2v,
    "hailuo_02_pro":       hailuo_02_pro_i2v,
    "hailuo_02_standard":  hailuo_02_standard_i2v,
    # Sora 2
    "sora2":               sora2_i2v,
    "sora2_pro":           sora2_pro_i2v,
    "sora2_characters":    sora2_characters_i2v,
    "sora2_characters_pro":sora2_characters_pro_i2v,
    # Wan
    "wan_2_6":             wan_2_6_i2v,
    "wan_2_6_flash":       wan_2_6_flash_i2v,
    "wan_2_5":             wan_2_5_i2v,
    "wan_2_2":             wan_2_2_i2v,
    # Veo 3.1
    "veo_3_1_fast":        lambda: veo_3_1_i2v("fast"),
    "veo_3_1_quality":     lambda: veo_3_1_i2v("quality"),
    # Runway
    "runway_10s":          lambda: runway_gen3_i2v(10),
    "runway_5s":           lambda: runway_gen3_i2v(5),
    # Grok
    "grok_imagine":        grok_imagine_i2v,
}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python kie_ai_i2v_reference.py <model_key>")
        print("       python kie_ai_i2v_reference.py all")
        print("\nAvailable models:")
        for k in ALL_MODELS:
            print(f"  {k}")
        sys.exit(0)

    target = sys.argv[1]

    if target == "all":
        results = {}
        for name, fn in ALL_MODELS.items():
            try:
                results[name] = fn()
            except Exception as e:
                results[name] = f"ERROR: {e}"
        print("\n=== Results ===")
        for k, v in results.items():
            print(f"  {k}: {v}")
    elif target in ALL_MODELS:
        video_url = ALL_MODELS[target]()
        print(f"\nVideo URL: {video_url}")
    else:
        print(f"Unknown model: {target}")
        sys.exit(1)