"""Run spectral co-clustering from the command line."""

from pathlib import Path

from .spectral_clustering import run_spectral_clustering


def main(config_path: str = "modeling_config.yaml"):
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    results = run_spectral_clustering(config_path)
    for name, path in results.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    import sys

    config_path = sys.argv[1] if len(sys.argv) > 1 else "modeling_config.yaml"
    main(config_path)
