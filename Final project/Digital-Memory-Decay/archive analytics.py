import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

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
# ARCHIVE ANALYTICS ENGINE
# ==========================================

class ArchiveAnalyticsEngine:


    def __init__(self):

        self.datasets = [

            "sample_dataset_1.csv",

            "sample_dataset_2.csv",

            "sample_dataset_3.csv",

            "sample_dataset_4.csv",

            "sample_dataset_5.csv"
        ]

        self.analytics_results = []

        os.makedirs(
            "outputs",
            exist_ok=True
        )

        os.makedirs(
            "reports",
            exist_ok=True
        )


    # ======================================
    # LOAD DATASETS
    # ======================================

    def load_all_datasets(self):

        loaded_datasets = []

        for dataset_name in self.datasets:

            dataset = load_dataset(
                dataset_name
            )

            loaded_datasets.append({

                "dataset_name":
                dataset_name,

                "data":
                dataset
            })

        return loaded_datasets


    # ======================================
    # ANALYZE SINGLE ARCHIVE
    # ======================================

    def analyze_archive(
        self,
        row
    ):

        access_frequency = row[
            "AccessFrequency"
        ]

        storage_condition = row[
            "StorageCondition"
        ]

        backup_status = row[
            "BackupStatus"
        ]

        initial_files = row[
            "InitialFiles"
        ]

        corruption_risk = row[
            "CorruptionRisk"
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

        return {

            "decay_rate":
            round(decay_rate, 3),

            "preservation_score":
            score,

            "risk_level":
            risk_level,

            "retention":
            retention
        }


    # ======================================
    # GENERATE FULL ANALYTICS
    # ======================================

    def generate_analytics(self):

        datasets = (
            self.load_all_datasets()
        )

        for dataset_object in datasets:

            dataset_name = dataset_object[
                "dataset_name"
            ]

            dataset = dataset_object[
                "data"
            ]

            for index, row in dataset.iterrows():

                archive_result = (
                    self.analyze_archive(row)
                )

                analytics_record = {

                    "dataset_name":
                    dataset_name,

                    "archive_id":
                    row["ArchiveID"],

                    "file_type":
                    row["FileType"],

                    "initial_files":
                    row["InitialFiles"],

                    "years_stored":
                    row["YearsStored"],

                    "decay_rate":
                    archive_result[
                        "decay_rate"
                    ],

                    "preservation_score":
                    archive_result[
                        "preservation_score"
                    ],

                    "risk_level":
                    archive_result[
                        "risk_level"
                    ]
                }

                self.analytics_results.append(
                    analytics_record
                )

        return pd.DataFrame(
            self.analytics_results
        )


    # ======================================
    # GENERATE ANALYTICS VISUALIZATIONS
    # ======================================

    def generate_visualizations(self):

        dataframe = pd.DataFrame(
            self.analytics_results
        )

        plt.style.use(
            "dark_background"
        )

        # ----------------------------------
        # PRESERVATION SCORE DISTRIBUTION
        # ----------------------------------

        plt.figure(
            figsize=(10, 6)
        )

        sns.histplot(

            dataframe[
                "preservation_score"
            ],

            bins=15,

            kde=True
        )

        plt.title(
            "Preservation Score Distribution"
        )

        plt.xlabel(
            "Preservation Score"
        )

        plt.ylabel(
            "Archive Count"
        )

        plt.tight_layout()

        plt.savefig(
            "outputs/preservation_distribution.png"
        )

        plt.close()


        # ----------------------------------
        # FILE TYPE ANALYSIS
        # ----------------------------------

        plt.figure(
            figsize=(12, 6)
        )

        filetype_scores = dataframe.groupby(
            "file_type"
        )[
            "preservation_score"
        ].mean()

        plt.bar(

            filetype_scores.index,

            filetype_scores.values
        )

        plt.title(
            "Average Preservation Score by File Type"
        )

        plt.xlabel(
            "File Type"
        )

        plt.ylabel(
            "Average Score"
        )

        plt.xticks(
            rotation=20
        )

        plt.tight_layout()

        plt.savefig(
            "outputs/filetype_analysis.png"
        )

        plt.close()


        # ----------------------------------
        # RISK LEVEL ANALYSIS
        # ----------------------------------

        risk_counts = dataframe[
            "risk_level"
        ].value_counts()

        plt.figure(
            figsize=(8, 8)
        )

        plt.pie(

            risk_counts.values,

            labels=risk_counts.index,

            autopct='%1.1f%%'
        )

        plt.title(
            "Archive Risk Distribution"
        )

        plt.tight_layout()

        plt.savefig(
            "outputs/risk_analysis.png"
        )

        plt.close()


        # ----------------------------------
        # DECAY RATE HEATMAP
        # ----------------------------------

        pivot_table = dataframe.pivot_table(

            values="decay_rate",

            index="file_type",

            columns="risk_level",

            aggfunc=np.mean
        )

        plt.figure(
            figsize=(10, 6)
        )

        sns.heatmap(

            pivot_table,

            annot=True,

            cmap="magma"
        )

        plt.title(
            "Decay Rate Heatmap"
        )

        plt.tight_layout()

        plt.savefig(
            "outputs/decay_heatmap.png"
        )

        plt.close()


        # ----------------------------------
        # STORAGE DURATION ANALYSIS
        # ----------------------------------

        plt.figure(
            figsize=(10, 6)
        )

        plt.scatter(

            dataframe[
                "years_stored"
            ],

            dataframe[
                "preservation_score"
            ],

            alpha=0.7
        )

        plt.title(
            "Storage Duration vs Preservation Score"
        )

        plt.xlabel(
            "Years Stored"
        )

        plt.ylabel(
            "Preservation Score"
        )

        plt.tight_layout()

        plt.savefig(
            "outputs/storage_duration_analysis.png"
        )

        plt.close()


    # ======================================
    # EXPORT ANALYTICS REPORT
    # ======================================

    def export_analytics_report(self):

        report_path = (
            "reports/archive_analytics_report.txt"
        )

        dataframe = pd.DataFrame(
            self.analytics_results
        )

        average_score = round(

            dataframe[
                "preservation_score"
            ].mean(),

            2
        )

        average_decay = round(

            dataframe[
                "decay_rate"
            ].mean(),

            3
        )

        critical_archives = len(

            dataframe[
                dataframe[
                    "risk_level"
                ] == "Critical"
            ]
        )

        moderate_archives = len(

            dataframe[
                dataframe[
                    "risk_level"
                ] == "Moderate"
            ]
        )

        low_archives = len(

            dataframe[
                dataframe[
                    "risk_level"
                ] == "Low"
            ]
        )

        with open(
            report_path,
            "w"
        ) as file:

            file.write(
                "DIGITAL ARCHIVE ANALYTICS REPORT\n\n"
            )

            file.write(

                f"Generated On: "
                f"{datetime.now()}\n\n"
            )

            file.write(

                f"Total Archives Processed: "
                f"{len(dataframe)}\n"
            )

            file.write(

                f"Average Preservation Score: "
                f"{average_score}%\n"
            )

            file.write(

                f"Average Decay Rate: "
                f"{average_decay}\n"
            )

            file.write(

                f"Critical Risk Archives: "
                f"{critical_archives}\n"
            )

            file.write(

                f"Moderate Risk Archives: "
                f"{moderate_archives}\n"
            )

            file.write(

                f"Low Risk Archives: "
                f"{low_archives}\n"
            )

            file.write(
                "\n=================================\n"
            )

        return report_path


# ==========================================
# MAIN EXECUTION ENGINE
# ==========================================

if __name__ == "__main__":

    analytics_engine = (
        ArchiveAnalyticsEngine()
    )

    analytics_dataframe = (

        analytics_engine
        .generate_analytics()
    )

    analytics_engine.generate_visualizations()

    report_location = (

        analytics_engine
        .export_analytics_report()
    )

    print(
        "\nARCHIVE ANALYTICS COMPLETED\n"
    )

    print(
        analytics_dataframe.head()
    )

    print(
        f"\nAnalytics Report Saved At:"
        f" {report_location}"
    )