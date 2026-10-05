from contextlib import redirect_stdout
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

from random_sleep import random_sleep
from timed_logged import TIMINGS


OUTPUT = Path(__file__).parent / "artifacts" / "runtime_distribution.png"
LOG_OUTPUT = Path(__file__).parent / "artifacts" / "benchmark.log"
SAMPLE_SIZES = (5, 25, 50, 100, 500, 5_000)
COLORS = ("#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9")


def plot_distributions(distributions):
    figure, axis = plt.subplots(figsize=(10.5, 6))
    maximum = max(max(durations) for durations in distributions.values())
    grid = np.linspace(0, maximum * 1.05, 500)

    for (size, durations), color in zip(distributions.items(), COLORS):
        durations = np.asarray(durations)
        axis.plot(grid, gaussian_kde(durations)(grid), color=color, linewidth=2.6, label=f"n = {size:,}".replace(",", " "))

    axis.set(title="Распределение фактического времени sleep", xlabel="Время, миллисекунды", ylabel="Плотность")
    axis.set_xlim(0, maximum * 1.05)
    axis.grid(axis="y", alpha=0.2)
    axis.legend(title="Число симуляций", frameon=False, ncol=3)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    figure.tight_layout()
    OUTPUT.parent.mkdir(exist_ok=True)
    figure.savefig(OUTPUT, dpi=180)
    plt.close(figure)


def run(seed=42):
    random.seed(seed)
    distributions = {}
    TIMINGS.clear()

    with LOG_OUTPUT.open("w") as log, redirect_stdout(log):
        for size in SAMPLE_SIZES:
            durations = []
            for _ in range(size):
                random_sleep(use_random_val=True)
                durations.append(TIMINGS[-1].elapsed_ms)
            distributions[size] = durations

    plot_distributions(distributions)
    print(f"График сохранён: {OUTPUT}")
    print(f"Логи вызовов сохранены: {LOG_OUTPUT}")


if __name__ == "__main__":
    run()
