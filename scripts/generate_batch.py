#!/usr/bin/env python3
"""
Batch video generation harness for all provider models.
Run without flags to execute all providers, or specify providers with --kling --sora etc.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROVIDERS = ["kling", "bytedance", "hailuo", "sora", "wan", "grok", "runway"]


def load_provider(name: str):
    """Load a provider module using importlib to avoid name collisions."""
    path = ROOT / name / "run.py"
    spec = importlib.util.spec_from_file_location(f"{name}_run", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load spec for {name}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"{name}_run"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_provider(provider_name: str, input_dir=None) -> dict:
    """Run all models for a single provider. Returns {model_key: result_path or ERROR}."""
    try:
        mod = load_provider(provider_name)
    except Exception as e:
        print(f"ERROR: Failed to load provider '{provider_name}': {e}")
        return {}
    if input_dir is not None:
        mod.INPUT_DIR = input_dir

    models = mod.MODELS
    provider = mod.PROVIDER
    results = {}

    print(f"\n=== Running: {provider} ({len(models)} models) ===")

    for key in models:
        try:
            dest = mod.run_model(key)
            results[key] = dest
        except Exception as e:
            print(f"[{provider}/{key}] ERROR: {e}")
            results[key] = f"ERROR: {e}"

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch run all video generation models across providers"
    )
    for provider in PROVIDERS:
        parser.add_argument(
            f"--{provider}",
            action="store_true",
            help=f"Run {provider} provider models",
        )
    parser.add_argument("--input", dest="input_dir", default=None,
                        help="Directory containing sample_image.jpeg and sample_prompt.txt (default: data/grass_sample/)")

    args = parser.parse_args()
    selected = [p for p in PROVIDERS if getattr(args, p)]

    if not selected:
        selected = PROVIDERS

    all_results = {}
    for provider_name in selected:
        results = run_provider(provider_name, input_dir=args.input_dir)
        all_results[provider_name] = results

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for provider, results in all_results.items():
        if results:
            print(f"\n{provider}:")
            for model_key, result in results.items():
                status = "OK" if isinstance(result, str) and not result.startswith("ERROR") else "FAIL"
                print(f"  [{status}] {model_key} → {result}")
        else:
            print(f"\n{provider}: (no results)")


if __name__ == "__main__":
    main()
