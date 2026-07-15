# Brent Oil Price Change Point Analysis

## Project Overview

This project analyzes historical Brent oil prices (1987–2022) using Bayesian change point detection to identify structural breaks caused by geopolitical and economic events.

## Repository Structure

- `notebooks/` – Jupyter notebook with EDA and modeling
- `src/` – Reusable Python modules
- `data/` – Raw data and events dataset
- `app.py` – Flask API for dashboard

## Requirements

Install dependencies: `pip install -r requirements.txt`

## Usage

1. Run the notebook: `jupyter notebook notebooks/01_EDA_and_ChangePoint.ipynb`
2. Start the dashboard: `python app.py` (then open <http://localhost:5000>)

## Results

- Most probable change point: 2013-04-11
- Mean log return before: 0.00017
- Mean log return after: 0.0005
- Estimated price impact: +0.033%

## Future Work

- Increase MCMC iterations for better convergence
- Implement multiple change point models
- Enhance dashboard with interactive filtering

## Author

Hawi Mekonen
