import argparse

__all__ = ("args",)

parser = argparse.ArgumentParser(description="GP_Backend Args")

parser.add_argument(
    "--mode", "-m", type=str, required=True, choices=["deploy", "dev", "front_dev"]
)

args = parser.parse_args()
