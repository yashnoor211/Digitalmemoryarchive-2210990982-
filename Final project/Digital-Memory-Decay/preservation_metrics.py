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


# ==========================================
# PRESERVATION SCORE ENGINE
# ==========================================

class PreservationScoreSystem:


    def __init__(self):

        self.datasets = [

            "sample_dataset_1.csv",

            "sample_dataset_2.csv",

            "sample_dataset_3.csv",

            "sample_dataset_4.csv",

            "sample_dataset_5.csv"
        ]

        self.output_directory = (
            "outputs"
        )

        self.preservation_results = []

        os.makedirs(
            self.output_directory,
            exist_ok=True
        )


    # ======================================
    # LOAD DATASETS
    # ======================================

    def load_all_datasets(self):

        loaded_datasets = []

        for dataset_name in self.datasets:

            dataset = load_dataset(

                f"datasets/{dataset_name}"
            )

            loaded_datasets.append({

                "dataset_name":
                dataset_name,

                "dataset":
                dataset
            })

        return loaded_datasets


    # ======================================
    # CALCULATE PRESERVATION SCORE
    # ======================================

    def calculate_preservation_score(

        self,

        initial_files,

        final_retention
    ):

        preservation_score = (

            final_retention
            /
            initial_files
        ) * 100

        return round(
            preservation_score,
            2
        )


    # ======================================
    # CLASSIFY PRESERVATION LEVEL
    # ======================================

    def classify_preservation_level(
        self,
        score
    ):

        if score >= 85:

            return "Excellent"

        elif score >= 70:

            return "Stable"

        elif score >= 50:

            return "Moderate"

        elif score >= 30:

            return "Vulnerable"

        return "Critical"


    # ======================================
    # PROCESS SINGLE ARCHIVE
    # ======================================

    def process_archive(
        self,
        dataset_name,
        row
    ):

        archive_id = row[
            "ArchiveID"
        ]

        file_type = row[
            "FileType"
        ]

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

        # ----------------------------------
        # DECAY RATE ANALYSIS
        # ----------------------------------

        decay_rate = get_decay_rate(

            access_frequency,

            storage_condition,

            corruption_risk,

            backup_status
        )

        # ----------------------------------
        # RETENTION SIMULATION
        # ----------------------------------

        retention = simulate_decay(

            initial_files,

            decay_rate,

            years_stored
        )

        final_retention = retention[-1]

        preservation_score = (

            self.calculate_preservation_score(

                initial_files,

                final_retention
            )
        )

        preservation_level = (

            self.classify_preservation_level(

                preservation_score
            )
        )

        return {

            "dataset_name":
            dataset_name,

            "archive_id":
            archive_id,

            "file_type":
            file_type,

            "initial_files":
            initial_files,

            "years_stored":
            years_stored,

            "decay_rate":
            round(decay_rate, 3),

            "final_retention":
            round(final_retention, 2),

            "preservation_score":
            preservation_score,

            "preservation_level":
            preservation_level
        }


    # ======================================
    # PROCESS ALL DATASETS
    # ======================================

    def process_all_datasets(self):

        datasets = (
            self.load_all_datasets()
        )

        for dataset_object in datasets:

            dataset_name = dataset_object[
                "dataset_name"
            ]

            dataset = dataset_object[
                "dataset"
            ]

            for index, row in dataset.iterrows():

                archive_result = (

                    self.process_archive(

                        dataset_name,

                        row
                    )
                )

                self.preservation_results.append(
                    archive_result
                )

        return pd.DataFrame(
            self.preservation_results
        )


    # ======================================
    # GENERATE VISUAL ANALYTICS
    # ======================================

    def generate_visual_analytics(self):

        dataframe = pd.DataFrame(
            self.preservation_results
        )

        plt.style.use(
            "dark_background"
        )

        # ----------------------------------
        # PRESERVATION DISTRIBUTION
        # ----------------------------------

        plt.figure(
            figsize=(12, 6)
        )

        sns.histplot(

            dataframe[
                "preservation_score"
            ],

            bins=20,

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

            f"{self.output_directory}/"
            f"preservation_distribution.png"
        )

        plt.close()


        # ----------------------------------
        # FILE TYPE SCORE ANALYSIS
        # ----------------------------------

        filetype_scores = dataframe.groupby(

            "file_type"

        )[
            "preservation_score"
        ].mean()

        plt.figure(
            figsize=(12, 6)
        )

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
            "Average Preservation Score"
        )

        plt.xticks(
            rotation=15
        )

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"filetype_preservation_analysis.png"
        )

        plt.close()


        # ----------------------------------
        # PRESERVATION HEATMAP
        # ----------------------------------

        heatmap_dataframe = dataframe.pivot_table(

            values="preservation_score",

            index="file_type",

            columns="preservation_level",

            aggfunc=np.mean
        )

        plt.figure(
            figsize=(10, 6)
        )

        sns.heatmap(

            heatmap_dataframe,

            annot=True,

            cmap="magma"
        )

        plt.title(
            "Preservation Level Heatmap"
        )

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"preservation_heatmap.png"
        )

        plt.close()


        # ----------------------------------
        # STORAGE DURATION IMPACT
        # ----------------------------------

        plt.figure(
            figsize=(12, 6)
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

            f"{self.output_directory}/"
            f"storage_duration_impact.png"
        )

        plt.close()


    # ======================================
    # EXPORT PRESERVATION REPORT
    # ======================================

    def export_preservation_report(self):

        report_path = (

            f"{self.output_directory}/"
            f"preservation_score_report.txt"
        )

        dataframe = pd.DataFrame(
            self.preservation_results
        )

        average_score = round(

            dataframe[
                "preservation_score"
            ].mean(),

            2
        )

        excellent_archives = len(

            dataframe[
                dataframe[
                    "preservation_level"
                ]
                ==
                "Excellent"
            ]
        )

        critical_archives = len(

            dataframe[
                dataframe[
                    "preservation_level"
                ]
                ==
                "Critical"
            ]
        )

        with open(
            report_path,
            "w"
        ) as file:

            file.write(
                "DIGITAL ARCHIVE "
                "PRESERVATION SCORE REPORT\n\n"
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

                f"Excellent Archives: "
                f"{excellent_archives}\n"
            )

            file.write(

                f"Critical Archives: "
                f"{critical_archives}\n"
            )

            file.write(
                "\n=====================================\n"
            )

        return report_path


# ==========================================
# MAIN EXECUTION ENGINE
# ==========================================

if __name__ == "__main__":

    preservation_engine = (
        PreservationScoreSystem()
    )

    preservation_dataframe = (

        preservation_engine
        .process_all_datasets()
    )

    preservation_engine.generate_visual_analytics()

    report_location = (

        preservation_engine
        .export_preservation_report()
    )

    print(
        "\nPRESERVATION SCORE ANALYSIS COMPLETED\n"
    )

    print(
        preservation_dataframe.head()
    )

    print(
        f"\nReport Exported To:"
        f" {report_location}"
    )