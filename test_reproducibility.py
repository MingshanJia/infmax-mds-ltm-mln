"""E2E test for runner to check reproducibly of results."""

from pathlib import Path

import pandas as pd
import pytest

from runners import main_runner
from runners.utils import set_rng_seed


@pytest.fixture
def tcase_config():
    return {
        "model": {
            "protocols": ["OR", "AND"],
            "mi_values": [0.9, 0.65, 0.1],
            "seed_budgets": [1, 10, 30],
            "ss_methods": ["deg_c", "random"],
        },
        "networks": ["toy_network"],
        "ranking_path": None,
        "run": {"max_epochs_num": 10, "patience": 1, "repetitions": 3, "random_seed": 1995},
        "logging": {"full_output_frequency": 1, "compress_to_zip": False, "out_dir": None},
    }


@pytest.fixture
def tcase_csv_names():
    return [
        Path("results--ver-1995_1.csv"),
        Path("results--ver-1995_2.csv"),
        Path("results--ver-1995_3.csv"),
    ]


def compare_results(gt_dir: Path, test_dir: Path, csv_names: list[str]) -> None:
    for csv_name in csv_names:
        gt_df = pd.read_csv(gt_dir / csv_name)
        test_df = pd.read_csv(test_dir / csv_name)
        pd.testing.assert_frame_equal(gt_df, test_df, obj=csv_name)
        print(f"Identity test passed for {csv_name}")
        check_integrity(test_df)
        print(f"Integrity test passed for {csv_name}")


def check_integrity(test_df: pd.DataFrame) -> None:
    test_df["er_temp"] = test_df["expositions_rec"].map(lambda x: x.split(";")).map(lambda x: [int(xx) for xx in x])
    assert test_df["seed_nb"].equals(test_df["seed_ids"].map(lambda x: x.split(";")).map(lambda x: len(x)))
    assert test_df["seed_nb"].equals(test_df["er_temp"].map(lambda x: x[0]))
    assert test_df["simulation_length"].equals(test_df["er_temp"].map(lambda x: len(x[:-1])))
    assert test_df["exposed_nb"].equals(test_df["er_temp"].map(lambda x: sum(x)))


def test_e2e(tcase_config, tcase_csv_names, tmpdir):
    tcase_config["logging"]["out_dir"] = str(tmpdir)
    set_rng_seed(tcase_config["run"]["random_seed"])
    main_runner.run_experiments(tcase_config)
    compare_results(Path("_test_data"), Path(tmpdir), tcase_csv_names)


if __name__ == "__main__":
    pytest.main(["-vs", __file__])