import pandas as pd


def create_features(df):

    df["avg_charge_per_month"] = (df["total_charges"] / (df["tenure_months"] + 1))

    return df