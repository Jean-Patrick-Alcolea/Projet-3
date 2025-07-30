import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def plot_meteo_forecast(data):
    hour_data = []
    for day in data["forecast"]["forecastday"]:
        for hour in day["hour"]:
            hour_data.append(
                {
                    "date": day["date"],
                    "hour": hour["time"],
                    "precipitation": hour["precip_mm"],
                }
            )
    df_hour = pd.DataFrame(hour_data)

    fig = px.area(
        df_hour,
        x="hour",
        y="precipitation",
        labels=False,
        title="Prévisions des Précipitations (en mm)",
    )
    fig.update_layout(
        title={
            "text": "Prévisions des Précipitations (en mm)",
            "font": {
                "family": "Open Sans",  # Police choisie
                "size": 24,  # Taille du titre
            },
            "x": 0.5,  # Centrer le titre
            "xanchor": "center",  # Ancrage du titre
        },
        xaxis_title=None,
        yaxis_title=None,
    )
    fig.update_traces(
        line_color="#57bb8a",
        fillcolor="rgba(87, 187, 138, 0.4)",  # couleur en semi-transparent
    )
    return fig
