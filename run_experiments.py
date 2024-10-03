# TODO: change prints to logs

import argparse
import yaml

from runners import main_runner
from runners.utils import set_rng_seed


def parse_args(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        help="Experiment config file (default: config.yaml).",
        type=str,
    )
    return parser.parse_args(*args)


if __name__ == "__main__":

    # uncomment for debugging
    # args = parse_args(["example_config.yaml"])

    # comment this line while debugging
    args = parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if random_seed := config["run"].get("random_seed"):
        print(f"Setting randomness seed as {random_seed}!")
        set_rng_seed(config["run"]["random_seed"])
    print(f"Loaded config: {config}")

    main_runner.run_experiments(config)