# Data Analysis Workflow for Brent Oil Price Change Point Detection

## 1. Data Loading & Cleaning
- Load `BrentOilPrices.csv` using Pandas.
- Parse `Date` column as datetime.
- Sort by date and set as index.
- Check for missing values and handle them (forward fill or drop).

## 2. Exploratory Data Analysis (EDA)
- Plot raw Brent oil prices over time to identify major trends and volatility.
- Compute daily log returns: `log(price_t) - log(price_{t-1})`.
- Plot log returns to observe volatility clustering.
- Perform Augmented Dickey-Fuller (ADF) test on log returns to confirm stationarity.

## 3. Event Compilation
- Research major geopolitical events, OPEC decisions, economic shocks (minimum 10-15).
- Store in `data/events.csv` with columns: `event_date`, `event_name`, `description`, `category`.
- Use these events later to associate detected change points with real-world causes.

## 4. Bayesian Change Point Model (PyMC)
- Define a switch point (`tau`) with a discrete uniform prior over all days.
- Define means before (`mu1`) and after (`mu2`) with Normal priors.
- Use `pm.math.switch` to choose the correct mean based on time index.
- Set likelihood as Normal with constant sigma.
- Run MCMC sampling (4 chains, 2000 draws, 2000 tune).
- Check convergence via `r_hat` and trace plots.

## 5. Interpretation
- Extract median `tau` to find the most likely change date.
- Compare `mu1` and `mu2` to quantify impact (percentage change).
- Match the change date with an event from `events.csv`.
- Formulate a narrative: *"On [date], the model detected a structural break coinciding with [event], resulting in a [X]% price change."*

## 6. Dashboard (Future Work)
- Build Flask APIs to serve price and event data.
- Create a React frontend with interactive charts showing price series and event markers.

## Assumptions & Limitations
- The model assumes a single change point; real price series may have multiple.
- Log returns are used to achieve stationarity; raw prices are non-stationary.
- Correlation does not imply causation – event association is tentative.
- The model assumes constant variance; future work may include GARCH components.
- Data ends in 2022; more recent events are not included.