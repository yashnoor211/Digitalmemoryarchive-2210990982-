import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import seaborn as sns

import os

from datetime import datetime

from data_preprocessing import (
    load_dataset
)


# ==========================================
# DATASET MANAGER SYSTEM
# ==========================================

class DatasetManagerSystem:


    def __init__(self):

        self.dataset_directory = (
            "datasets"
        )

        self.output_directory = (
            "outputs"
        )

        self.datasets = [

            "sample_dataset_1.csv",

            "sample_dataset_2.csv",

            "sample_dataset_3.csv",

            "sample_dataset_4.csv",

            "sample_dataset_5.csv"
        ]

        self.dataset_reports = []

        os.makedirs(
            self.output_directory,
            exist_ok=True
        )


    # ======================================
    # LOAD ALL DATASETS
    # ======================================

    def load_all_datasets(self):

        loaded_datasets = []

        for dataset_name in self.datasets:

            dataset_path = (

                f"{self.dataset_directory}/"
                f"{dataset_name}"
            )

            dataset = load_dataset(
                dataset_path
            )

            loaded_datasets.append({

                "dataset_name":
                dataset_name,

                "dataset":
                dataset
            })

        return loaded_datasets


    # ======================================
    # GENERATE DATASET STATISTICS
    # ======================================

    def generate_dataset_statistics(
        self,
        dataset_name,
        dataset
    ):

        total_rows = len(dataset)

        total_columns = len(
            dataset.columns
        )

        total_files = int(

            dataset[
                "InitialFiles"
            ].sum()
        )

        average_corruption = round(

            dataset[
                "CorruptionRisk"
            ].mean(),

            3
        )

        average_access_frequency = round(

            dataset[
                "AccessFrequency"
            ].mean(),

            2
        )

        average_storage_duration = round(

            dataset[
                "YearsStored"
            ].mean(),

            2
        )

        most_common_file_type = (

            dataset[
                "FileType"
            ].mode()[0]
        )

        dataset_size = round(

            dataset.memory_usage(
                deep=True
            ).sum()
            /
            1024,

            2
        )

        report = {

            "dataset_name":
            dataset_name,

            "rows":
            total_rows,

            "columns":
            total_columns,

            "total_files":
            total_files,

            "average_corruption":
            average_corruption,

            "average_access_frequency":
            average_access_frequency,

            "average_storage_duration":
            average_storage_duration,

            "most_common_file_type":
            most_common_file_type,

            "dataset_size_kb":
            dataset_size
        }

        return report


    # ======================================
    # PROCESS DATASETS
    # ======================================

    def process_datasets(self):

        loaded_datasets = (
            self.load_all_datasets()
        )

        for dataset_object in loaded_datasets:

            dataset_name = dataset_object[
                "dataset_name"
            ]

            dataset = dataset_object[
                "dataset"
            ]

            report = (
                self.generate_dataset_statistics(

                    dataset_name,

                    dataset
                )
            )

            self.dataset_reports.append(
                report
            )

        return pd.DataFrame(
            self.dataset_reports
        )


    # ======================================
    # GENERATE DATASET VISUALIZATION
    # ======================================

    def generate_visualizations(self):

        dataframe = pd.DataFrame(
            self.dataset_reports
        )

        plt.style.use(
            "dark_background"
        )

        # ----------------------------------
        # DATASET SIZE ANALYSIS
        # ----------------------------------

        plt.figure(
            figsize=(12, 6)
        )

        plt.bar(

            dataframe[
                "dataset_name"
            ],

            dataframe[
                "dataset_size_kb"
            ]
        )

        plt.title(
            "Dataset Size Distribution"
        )

        plt.xlabel(
            "Datasets"
        )

        plt.ylabel(
            "Dataset Size (KB)"
        )

        plt.xticks(
            rotation=15
        )

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"dataset_size_analysis.png"
        )

        plt.close()


        # ----------------------------------
        # FILE DISTRIBUTION ANALYSIS
        # ----------------------------------

        plt.figure(
            figsize=(12, 6)
        )

        plt.plot(

            dataframe[
                "dataset_name"
            ],

            dataframe[
                "total_files"
            ],

            marker='o',

            linewidth=3
        )

        plt.title(
            "Dataset File Distribution"
        )

        plt.xlabel(
            "Datasets"
        )

        plt.ylabel(
            "Total Files"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"file_distribution_analysis.png"
        )

        plt.close()


        # ----------------------------------
        # CORRUPTION HEATMAP
        # ----------------------------------

        heatmap_dataframe = pd.DataFrame({

            "Corruption Risk":

            dataframe[
                "average_corruption"
            ],

            "Storage Duration":

            dataframe[
                "average_storage_duration"
            ],

            "Access Frequency":

            dataframe[
                "average_access_frequency"
            ]
        },

        index=dataframe[
            "dataset_name"
        ])

        plt.figure(
            figsize=(10, 6)
        )

        sns.heatmap(

            heatmap_dataframe,

            annot=True,

            cmap="magma"
        )

        plt.title(
            "Dataset Management Heatmap"
        )

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"dataset_heatmap.png"
        )

        plt.close()


    # ======================================
    # EXPORT DATASET REPORT
    # ======================================

    def export_dataset_report(self):

        report_path = (

            f"{self.output_directory}/"
            f"dataset_manager_report.txt"
        )

        with open(
            report_path,
            "w"
        ) as file:

            file.write(
                "DIGITAL ARCHIVE "
                "DATASET MANAGER REPORT\n\n"
            )

            file.write(

                f"Generated On: "
                f"{datetime.now()}\n\n"
            )

            for report in self.dataset_reports:

                file.write(

                    f"Dataset Name: "
                    f"{report['dataset_name']}\n"
                )

                file.write(

                    f"Rows: "
                    f"{report['rows']}\n"
                )

                file.write(

                    f"Columns: "
                    f"{report['columns']}\n"
                )

                file.write(

                    f"Total Files: "
                    f"{report['total_files']}\n"
                )

                file.write(

                    f"Average Corruption Risk: "
                    f"{report['average_corruption']}\n"
                )

                file.write(

                    f"Average Access Frequency: "
                    f"{report['average_access_frequency']}\n"
                )

                file.write(

                    f"Average Storage Duration: "
                    f"{report['average_storage_duration']}\n"
                )

                file.write(

                    f"Most Common File Type: "
                    f"{report['most_common_file_type']}\n"
                )

                file.write(

                    f"Dataset Size: "
                    f"{report['dataset_size_kb']} KB\n"
                )

                file.write(
                    "\n====================================\n\n"
                )

        return report_path


    # ======================================
    # DATASET SEARCH ENGINE
    # ======================================

    def search_archive_by_id(
        self,
        archive_id
    ):

        loaded_datasets = (
            self.load_all_datasets()
        )

        for dataset_object in loaded_datasets:

            dataset_name = dataset_object[
                "dataset_name"
            ]

            dataset = dataset_object[
                "dataset"
            ]

            matching_archive = dataset[

                dataset[
                    "ArchiveID"
                ]
                ==
                archive_id
            ]

            if not matching_archive.empty:

                return {

                    "dataset_name":
                    dataset_name,

                    "archive_data":
                    matching_archive.to_dict(
                        orient="records"
                    )[0]
                }

        return None


# ==========================================
# MAIN EXECUTION ENGINE
# ==========================================

if __name__ == "__main__":

    dataset_manager = (
        DatasetManagerSystem()
    )

    dataset_dataframe = (

        dataset_manager
        .process_datasets()
    )

    dataset_manager.generate_visualizations()

    report_location = (

        dataset_manager
        .export_dataset_report()
    )

    print(
        "\nDATASET MANAGER EXECUTION COMPLETED\n"
    )

    print(
        dataset_dataframe
    )

    print(
        f"\nReport Exported To:"
        f" {report_location}"
    )

    # --------------------------------------
    # SAMPLE SEARCH ENGINE
    # --------------------------------------

    archive_search = (

        dataset_manager
        .search_archive_by_id(
            "AR1001"
        )
    )

    print(
        "\nARCHIVE SEARCH RESULT:\n"
    )

    print(
        archive_search
    )