import subprocess
import sys


PIPELINE = [
    ("Benchmark", "src/evaluation/benchmark.py"),
    ("Report", "src/evaluation/report.py"),
    ("Metrics", "src/evaluation/metrics.py"),
    ("LLM Judge", "src/evaluation/judge.py")
]


def run_stage(name, script):

    print(f"\n{'--->'}")
    print(f"Running: {name}")
    print(f"{'--->'}\n")

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:

        raise RuntimeError(
            f"{name} failed."
        )


def main():

    for stage in PIPELINE:

        run_stage(*stage)

    print("\nEvaluation pipeline complete.")


if __name__ == "__main__":

    main()