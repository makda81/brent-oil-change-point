import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import pytensor
import os

# Force pure Python mode (no compilation)
os.environ['PYTENSOR_FLAGS'] = 'mode=FAST_RUN,linker=vm,cxx=""'
pytensor.config.mode = 'FAST_RUN'
pytensor.config.link = 'vm'
pytensor.config.cxx = ''


def load_data(filepath):
    """Load Brent oil prices and compute log returns."""
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)
    df.set_index('Date', inplace=True)
    df['log_return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
    df.dropna(inplace=True)
    return df


def run_change_point_model(y):
    """
    Run Bayesian change point model on log returns.
    Returns trace and model object.
    """
    n = len(y)
    time_idx = np.arange(n)
    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)
        mu1 = pm.Normal('mu1', mu=0, sigma=0.5)
        mu2 = pm.Normal('mu2', mu=0, sigma=0.5)
        sigma = pm.HalfNormal('sigma', sigma=0.5)
        mu = pm.math.switch(time_idx < tau, mu1, mu2)
        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=y)
        trace = pm.sample(500, tune=500, chains=2, cores=1, return_inferencedata=True)
    return trace, model


def get_change_point(trace, df):
    """Extract the most probable change point date and impact."""
    tau_median = int(np.median(trace.posterior['tau']))
    change_date = df.index[tau_median]
    mu1_mean = trace.posterior['mu1'].mean().item()
    mu2_mean = trace.posterior['mu2'].mean().item()
    impact_pct = (np.exp(mu2_mean - mu1_mean) - 1) * 100
    return change_date, mu1_mean, mu2_mean, impact_pct


def load_events(filepath):
    """Load events CSV."""
    events = pd.read_csv(filepath, parse_dates=['event_date'])
    return events