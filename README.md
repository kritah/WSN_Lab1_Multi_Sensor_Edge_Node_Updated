# WSN Lab 1: Multi-Sensor Edge Node Data Analysis

This repository contains the sensor dataset and reproducible Python analysis for the
Wireless Sensor Networks Lab 1 project.

## Dataset

`data/WSN_Lab1_Combined_Updated_LDR.csv` contains 600 samples and 17 columns.
The corrected LDR readings have been inserted into the original dataset by row order.
The recordings should not be treated as simultaneous unless independently verified.

Important measurement notes:
- `timestamp` is ESP32 elapsed time in seconds since boot.
- `temp` and `humidity` are DHT measurements.
- `light` is a normalised LDR reading from 0 to 1. It is not measured in lux.
- `motion` is the PIR state: 0 means no motion and 1 means motion.
- `temp_cal` is the calibrated temperature column in the supplied dataset.
- `temp_filt` is the filtered temperature.
- `delta_temp` is the change between accepted fresh temperature readings.
- `ref_temp` is the LM35 reference temperature.
- `valid` indicates whether the DHT reading is valid.
- `dht_fresh` indicates whether a new DHT read was attempted.
- `event` marks an event transition.

## Requirements

- Python 3.9 or later
- pandas
- matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the analysis

From the repository root, run:

```bash
python analysis/analyze_sensor_data.py
```

The script generates:
- Six PNG graphs in `results/figures/`
- `results/summary_statistics.csv`
- `results/data_quality_summary.txt`

## Suggested repository structure

```text
WSN_Lab1_Git_Repository/
├── analysis/
│   └── analyze_sensor_data.py
├── data/
│   └── WSN_Lab1_Combined_Updated_LDR.csv
├── results/
│   └── figures/
├── requirements.txt
└── README.md
```

## Push to GitHub

Create an empty GitHub repository first. Then open a terminal in this folder and run:

```bash
git init
git add .
git commit -m "Add WSN Lab 1 sensor data analysis"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with the HTTPS URL of your own GitHub repository.

If Git reports that `origin` already exists, use:

```bash
git remote set-url origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
