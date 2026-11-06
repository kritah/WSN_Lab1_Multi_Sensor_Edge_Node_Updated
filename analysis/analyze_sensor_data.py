"""
Wireless Sensor Networks Lab 1
Multi-Sensor Edge Node: Sensor Data Analysis

Run from the repository root:
    python analysis/analyze_sensor_data.py

Input:
    data/WSN_Lab1_Combined_Updated_LDR.csv

Outputs:
    results/figures/*.png
    results/summary_statistics.csv
    results/data_quality_summary.txt
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "WSN_Lab1_Combined_Updated_LDR.csv"
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"

RESULTS_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def save_plot(filename):
    """Save the current Matplotlib figure in the results/figures folder."""
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()


def main():
    # 1. Load the dataset
    df = pd.read_csv(DATA_FILE)

    print("\nDATASET OVERVIEW")
    print("----------------")
    print("Rows and columns:", df.shape)
    print("\nFirst five rows:")
    print(df.head())
    print("\nColumn names:")
    print(df.columns.tolist())

    # 2. Convert measurement columns to numeric safely.
    numeric_columns = [
        "timestamp", "temp", "humidity", "light", "motion",
        "temp_cal", "temp_filt", "delta_temp", "valid",
        "dht_fresh", "event", "ref_temp", "t_s"
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # Keep the original row order, which represents the recorded samples.
    # The updated LDR values were aligned to the original dataset by row number.
    if "timestamp" in df.columns:
        df = df.sort_values("timestamp").reset_index(drop=True)

    # 3. Data quality checks
    missing = df.isna().sum()
    valid_count = int(df["valid"].fillna(0).eq(1).sum()) if "valid" in df else 0
    invalid_count = int(df["valid"].fillna(0).eq(0).sum()) if "valid" in df else 0
    motion_count = int(df["motion"].fillna(0).eq(1).sum()) if "motion" in df else 0
    event_count = int(df["event"].fillna(0).eq(1).sum()) if "event" in df else 0

    quality_lines = [
        "WIRELESS SENSOR NETWORKS LAB 1 - DATA QUALITY SUMMARY",
        "=" * 58,
        f"Number of rows: {len(df)}",
        f"Number of columns: {len(df.columns)}",
        f"Valid DHT rows (valid=1): {valid_count}",
        f"Invalid DHT rows (valid=0): {invalid_count}",
        f"Rows indicating motion (motion=1): {motion_count}",
        f"Event transitions (event=1): {event_count}",
        "",
        "Missing values per column:",
        missing.to_string(),
        "",
        "NOTE: The light column contains normalised LDR readings (0 to 1).",
        "These values are not lux measurements.",
        "NOTE: The corrected LDR file was merged with the original dataset",
        "by row order. The two recordings should not be interpreted as",
        "simultaneous measurements unless independently verified."
    ]
    (RESULTS_DIR / "data_quality_summary.txt").write_text(
        "\n".join(quality_lines), encoding="utf-8"
    )

    print("\nDATA QUALITY")
    print("------------")
    print(missing)
    print(f"\nValid rows: {valid_count}; Invalid rows: {invalid_count}")
    print(f"Motion rows: {motion_count}; Event transitions: {event_count}")

    # 4. Descriptive statistics
    measurement_columns = [
        c for c in ["temp", "humidity", "light", "temp_cal",
                    "temp_filt", "delta_temp", "ref_temp"]
        if c in df.columns
    ]
    stats = df[measurement_columns].describe().T
    stats.to_csv(RESULTS_DIR / "summary_statistics.csv")
    print("\nSUMMARY STATISTICS")
    print("------------------")
    print(stats)

    # 5. Temperature against elapsed ESP32 time
    if {"timestamp", "temp"}.issubset(df.columns):
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["temp"], label="DHT temperature")
        if "ref_temp" in df.columns:
            plt.plot(df["timestamp"], df["ref_temp"], label="LM35 reference", alpha=0.8)
        plt.xlabel("ESP32 timestamp (seconds since boot)")
        plt.ylabel("Temperature (°C)")
        plt.title("Temperature Readings Over Time")
        plt.grid(True)
        plt.legend()
        save_plot("01_temperature_vs_time.png")

    # 6. Humidity against elapsed time
    if {"timestamp", "humidity"}.issubset(df.columns):
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["humidity"])
        plt.xlabel("ESP32 timestamp (seconds since boot)")
        plt.ylabel("Relative humidity (%)")
        plt.title("Humidity Readings Over Time")
        plt.grid(True)
        save_plot("02_humidity_vs_time.png")

    # 7. Raw/calibrated and filtered temperature
    if {"timestamp", "temp_cal", "temp_filt"}.issubset(df.columns):
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["temp_cal"], label="Calibrated temperature", alpha=0.65)
        plt.plot(df["timestamp"], df["temp_filt"], label="Filtered temperature", linewidth=2)
        plt.xlabel("ESP32 timestamp (seconds since boot)")
        plt.ylabel("Temperature (°C)")
        plt.title("Effect of Moving-Average Filtering")
        plt.grid(True)
        plt.legend()
        save_plot("03_calibrated_vs_filtered_temperature.png")

    # 8. Normalised LDR readings
    if {"timestamp", "light"}.issubset(df.columns):
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["light"])
        plt.xlabel("ESP32 timestamp (seconds since boot)")
        plt.ylabel("Normalised LDR reading (0 to 1)")
        plt.title("Light Sensor Response Over Time")
        plt.ylim(0, 1.05)
        plt.grid(True)
        save_plot("04_light_vs_time.png")

    # 9. PIR motion state
    if {"timestamp", "motion"}.issubset(df.columns):
        plt.figure(figsize=(10, 3.5))
        plt.step(df["timestamp"], df["motion"], where="post")
        plt.xlabel("ESP32 timestamp (seconds since boot)")
        plt.ylabel("PIR state (0 = no motion, 1 = motion)")
        plt.title("PIR Motion Detection")
        plt.yticks([0, 1], ["No motion", "Motion"])
        plt.ylim(-0.15, 1.15)
        plt.grid(True)
        save_plot("05_motion_detection.png")

    # 10. Event transitions
    if {"timestamp", "event"}.issubset(df.columns):
        event_rows = df[df["event"].eq(1)]
        plt.figure(figsize=(10, 4))
        plt.scatter(event_rows["timestamp"], event_rows["event"])
        plt.xlabel("ESP32 timestamp (seconds since boot)")
        plt.ylabel("Event")
        plt.title("Detected Event Transitions")
        plt.yticks([1], ["Event"])
        plt.ylim(0.5, 1.5)
        plt.grid(True)
        save_plot("06_event_transitions.png")

    print("\nAnalysis complete.")
    print(f"Figures and summaries have been saved in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
