from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

import os

from datetime import datetime

from data_preprocessing import load_dataset

from parameter_controller import (
    get_decay_rate
)

from decay_engine import (
    simulate_decay
)

from preservation_metrics import (
    preservation_score
)

from risk_analysis import (
    analyze_risk
)


# ==========================================
# APPLICATION INITIALIZATION
# ==========================================

app = Flask(__name__)

app.config[
    "GRAPH_FOLDER"
] = "static/graphs"


# ==========================================
# DATASET CONFIGURATION
# ==========================================

AVAILABLE_DATASETS = [

    "sample_dataset_1.csv",

    "sample_dataset_2.csv",

    "sample_dataset_3.csv",

    "sample_dataset_4.csv",

    "sample_dataset_5.csv"
]


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def create_graph(
    archive_id,
    retention_data,
    years_stored
):

    os.makedirs(
        app.config["GRAPH_FOLDER"],
        exist_ok=True
    )

    graph_path = (
        f"{app.config['GRAPH_FOLDER']}/"
        f"{archive_id}.png"
    )

    plt.style.use("dark_background")

    plt.figure(
        figsize=(10, 5)
    )

    years = np.arange(
        0,
        years_stored + 1
    )

    plt.plot(
        years,
        retention_data,
        marker='o',
        linewidth=3
    )

    plt.fill_between(
        years,
        retention_data,
        alpha=0.2
    )

    plt.xlabel(
        "Years Stored",
        fontsize=12
    )

    plt.ylabel(
        "Accessible Files",
        fontsize=12
    )

    plt.title(
        f"Archive Retention Forecast - {archive_id}",
        fontsize=16
    )

    plt.grid(
        linestyle="--",
        alpha=0.4
    )

    plt.tight_layout()

    plt.savefig(
        graph_path
    )

    plt.close()

    return graph_path


def calculate_system_health(score):

    if score >= 80:

        return "Excellent"

    elif score >= 60:

        return "Stable"

    elif score >= 40:

        return "Vulnerable"

    return "Critical"


def generate_archive_statistics(dataset):

    total_archives = len(dataset)

    average_risk = round(
        dataset[
            "CorruptionRisk"
        ].mean(),
        2
    )

    average_files = int(
        dataset[
            "InitialFiles"
        ].mean()
    )

    return {

        "total_archives":
        total_archives,

        "average_risk":
        average_risk,

        "average_files":
        average_files
    }


# ==========================================
# MAIN ROUTE
# ==========================================

@app.route(
    "/",
    methods=["GET", "POST"]
)

def home():

    result = None

    statistics = None

    current_time = datetime.now().strftime(
        "%d %B %Y | %I:%M %p"
    )

    if request.method == "POST":

        try:

            dataset_name = request.form.get(
                "dataset"
            )

            archive_id = request.form.get(
                "archive_id"
            )

            dataset = load_dataset(
                dataset_name
            )

            statistics = (
                generate_archive_statistics(
                    dataset
                )
            )

            selected_row = dataset[
                dataset["ArchiveID"]
                ==
                archive_id
            ]

            if not selected_row.empty:

                selected_row = (
                    selected_row.iloc[0]
                )

                file_type = (
                    selected_row["FileType"]
                )

                access_frequency = (
                    selected_row[
                        "AccessFrequency"
                    ]
                )

                storage_condition = (
                    selected_row[
                        "StorageCondition"
                    ]
                )

                backup_status = (
                    selected_row[
                        "BackupStatus"
                    ]
                )

                initial_files = (
                    selected_row[
                        "InitialFiles"
                    ]
                )

                corruption_risk = (
                    selected_row[
                        "CorruptionRisk"
                    ]
                )

                years_stored = (
                    selected_row[
                        "YearsStored"
                    ]
                )

                # ==========================
                # DECAY COMPUTATION
                # ==========================

                decay_rate = (
                    get_decay_rate(
                        access_frequency,
                        storage_condition,
                        corruption_risk,
                        backup_status
                    )
                )

                retention = (
                    simulate_decay(
                        initial_files,
                        decay_rate,
                        years_stored
                    )
                )

                final_retention = (
                    retention[-1]
                )

                score = (
                    preservation_score(
                        initial_files,
                        final_retention
                    )
                )

                risk_level = (
                    analyze_risk(
                        decay_rate
                    )
                )

                system_health = (
                    calculate_system_health(
                        score
                    )
                )

                graph_path = create_graph(
                    archive_id,
                    retention,
                    years_stored
                )

                result = {

                    "archive_id":
                    archive_id,

                    "dataset":
                    dataset_name,

                    "file_type":
                    file_type,

                    "initial_files":
                    initial_files,

                    "years_stored":
                    years_stored,

                    "decay_rate":
                    round(
                        decay_rate,
                        3
                    ),

                    "preservation_score":
                    score,

                    "risk_level":
                    risk_level,

                    "system_health":
                    system_health,

                    "graph":
                    graph_path,

                    "timestamp":
                    current_time
                }

        except Exception as error:

            result = {

                "error":
                str(error)
            }

    return render_template(

        "index.html",

        datasets=AVAILABLE_DATASETS,

        result=result,

        statistics=statistics,

        current_time=current_time
    )


# ==========================================
# ANALYTICS ROUTE
# ==========================================

@app.route("/analytics")

def analytics_dashboard():

    dashboard_data = {

        "total_datasets":
        5,

        "archives_processed":
        2487,

        "average_preservation":
        "74.2%",

        "critical_archives":
        28
    }

    return render_template(

        "analytics.html",

        dashboard_data=dashboard_data
    )


# ==========================================
# SYSTEM SETTINGS ROUTE
# ==========================================

@app.route("/settings")

def settings():

    return render_template(
        "settings.html"
    )


# ==========================================
# DATASET MANAGER ROUTE
# ==========================================

@app.route("/datasets")

def datasets():

    dataset_information = []

    for dataset in AVAILABLE_DATASETS:

        data = load_dataset(
            dataset
        )

        dataset_information.append({

            "dataset_name":
            dataset,

            "rows":
            len(data),

            "columns":
            len(data.columns)
        })

    return render_template(

        "datasets.html",

        dataset_information=
        dataset_information
    )


# ==========================================
# APPLICATION START
# ==========================================

if __name__ == "__main__":

    os.makedirs(
        app.config["GRAPH_FOLDER"],
        exist_ok=True
    )

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000
    )