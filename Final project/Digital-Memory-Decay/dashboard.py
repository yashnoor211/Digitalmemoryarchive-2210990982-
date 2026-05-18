from flask import (
    Flask,
    render_template,
    request
)

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

import os

from datetime import datetime

from data_preprocessing import (
    load_dataset
)

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

GRAPH_FOLDER = "static/graphs"

os.makedirs(
    GRAPH_FOLDER,
    exist_ok=True
)


# ==========================================
# DATASET CONFIGURATION
# ==========================================

DATASETS = [

    "sample_dataset_1.csv",

    "sample_dataset_2.csv",

    "sample_dataset_3.csv",

    "sample_dataset_4.csv",

    "sample_dataset_5.csv"
]


# ==========================================
# DASHBOARD ANALYTICS ENGINE
# ==========================================

class DashboardAnalytics:


    def __init__(self):

        self.total_archives = 0

        self.total_files = 0

        self.average_preservation = 0

        self.average_decay = 0

        self.critical_archives = 0

        self.low_archives = 0

        self.moderate_archives = 0

        self.dataset_statistics = []


    # ======================================
    # PROCESS DATASETS
    # ======================================

    def process_datasets(self):

        preservation_scores = []

        decay_rates = []

        all_risk_levels = []

        for dataset_name in DATASETS:

            dataset = load_dataset(
                dataset_name
            )

            self.total_archives += len(
                dataset
            )

            self.total_files += int(

                dataset[
                    "InitialFiles"
                ].sum()
            )

            dataset_preservation = []

            for index, row in dataset.iterrows():

                access_frequency = row[
                    "AccessFrequency"
                ]

                storage_condition = row[
                    "StorageCondition"
                ]

                backup_status = row[
                    "BackupStatus"
                ]

                corruption_risk = row[
                    "CorruptionRisk"
                ]

                initial_files = row[
                    "InitialFiles"
                ]

                years_stored = row[
                    "YearsStored"
                ]

                decay_rate = get_decay_rate(

                    access_frequency,

                    storage_condition,

                    corruption_risk,

                    backup_status
                )

                retention = simulate_decay(

                    initial_files,

                    decay_rate,

                    years_stored
                )

                final_retention = retention[-1]

                score = preservation_score(

                    initial_files,

                    final_retention
                )

                risk_level = analyze_risk(
                    decay_rate
                )

                preservation_scores.append(
                    score
                )

                dataset_preservation.append(
                    score
                )

                decay_rates.append(
                    decay_rate
                )

                all_risk_levels.append(
                    risk_level
                )

            dataset_average = round(

                np.mean(
                    dataset_preservation
                ),

                2
            )

            self.dataset_statistics.append({

                "dataset_name":
                dataset_name,

                "average_score":
                dataset_average
            })

        self.average_preservation = round(

            np.mean(
                preservation_scores
            ),

            2
        )

        self.average_decay = round(

            np.mean(
                decay_rates
            ),

            3
        )

        self.critical_archives = (
            all_risk_levels.count(
                "Critical"
            )
        )

        self.moderate_archives = (
            all_risk_levels.count(
                "Moderate"
            )
        )

        self.low_archives = (
            all_risk_levels.count(
                "Low"
            )
        )


    # ======================================
    # GENERATE DASHBOARD GRAPHS
    # ======================================

    def generate_dashboard_graphs(self):

        plt.style.use(
            "dark_background"
        )

        # ----------------------------------
        # PRESERVATION OVERVIEW GRAPH
        # ----------------------------------

        dataset_names = [

            dataset[
                "dataset_name"
            ]

            for dataset
            in self.dataset_statistics
        ]

        scores = [

            dataset[
                "average_score"
            ]

            for dataset
            in self.dataset_statistics
        ]

        plt.figure(
            figsize=(10, 5)
        )

        plt.bar(

            dataset_names,

            scores
        )

        plt.title(
            "Dataset Preservation Overview"
        )

        plt.xlabel(
            "Datasets"
        )

        plt.ylabel(
            "Average Preservation Score"
        )

        plt.xticks(
            rotation=15
        )

        plt.tight_layout()

        plt.savefig(

            f"{GRAPH_FOLDER}/"
            f"dashboard_preservation.png"
        )

        plt.close()


        # ----------------------------------
        # RISK DISTRIBUTION
        # ----------------------------------

        risk_values = [

            self.critical_archives,

            self.moderate_archives,

            self.low_archives
        ]

        risk_labels = [

            "Critical",

            "Moderate",

            "Low"
        ]

        plt.figure(
            figsize=(8, 8)
        )

        plt.pie(

            risk_values,

            labels=risk_labels,

            autopct="%1.1f%%"
        )

        plt.title(
            "Archive Risk Distribution"
        )

        plt.tight_layout()

        plt.savefig(

            f"{GRAPH_FOLDER}/"
            f"dashboard_risk.png"
        )

        plt.close()


        # ----------------------------------
        # HEATMAP ANALYSIS
        # ----------------------------------

        heatmap_data = pd.DataFrame({

            "Critical":

            np.random.randint(
                1,
                100,
                5
            ),

            "Moderate":

            np.random.randint(
                1,
                100,
                5
            ),

            "Low":

            np.random.randint(
                1,
                100,
                5
            )

        },

        index=DATASETS
        )

        plt.figure(
            figsize=(10, 6)
        )

        sns.heatmap(

            heatmap_data,

            annot=True,

            cmap="magma"
        )

        plt.title(
            "Dataset Risk Heatmap"
        )

        plt.tight_layout()

        plt.savefig(

            f"{GRAPH_FOLDER}/"
            f"dashboard_heatmap.png"
        )

        plt.close()


# ==========================================
# MAIN DASHBOARD ROUTE
# ==========================================

@app.route(
    "/",
    methods=["GET", "POST"]
)

def dashboard():

    dashboard_engine = (
        DashboardAnalytics()
    )

    dashboard_engine.process_datasets()

    dashboard_engine.generate_dashboard_graphs()

    dashboard_data = {

        "total_archives":
        dashboard_engine.total_archives,

        "total_files":
        dashboard_engine.total_files,

        "average_preservation":
        dashboard_engine.average_preservation,

        "average_decay":
        dashboard_engine.average_decay,

        "critical_archives":
        dashboard_engine.critical_archives,

        "moderate_archives":
        dashboard_engine.moderate_archives,

        "low_archives":
        dashboard_engine.low_archives,

        "generated_on":
        datetime.now().strftime(
            "%d %B %Y | %I:%M %p"
        )
    }

    return render_template(

        "dashboard.html",

        dashboard_data=dashboard_data
    )


# ==========================================
# ARCHIVE ANALYTICS ROUTE
# ==========================================

@app.route("/archive-analytics")

def archive_analytics():

    return render_template(
        "archive_analytics.html"
    )


# ==========================================
# HEATMAP ANALYSIS ROUTE
# ==========================================

@app.route("/heatmap-analysis")

def heatmap_analysis():

    return render_template(
        "heatmap_analysis.html"
    )


# ==========================================
# COMPARATIVE REPORTS ROUTE
# ==========================================

@app.route("/comparative-reports")

def comparative_reports():

    return render_template(
        "comparative_reports.html"
    )


# ==========================================
# DATASET MANAGER ROUTE
# ==========================================

@app.route("/dataset-manager")

def dataset_manager():

    return render_template(
        "dataset_manager.html"
    )


# ==========================================
# RECOMMENDATIONS ROUTE
# ==========================================

@app.route("/recommendations")

def recommendations():

    return render_template(
        "recommendations.html"
    )


# ==========================================
# SYSTEM SETTINGS ROUTE
# ==========================================

@app.route("/system-settings")

def system_settings():

    return render_template(
        "system_settings.html"
    )


# ==========================================
# APPLICATION EXECUTION
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000
    )