import pandas as pd

import matplotlib.pyplot as plt

import numpy as np

import os

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
# COMPARATIVE ANALYSIS ENGINE
# ==========================================

class ComparativeAnalysisSystem:


    def __init__(self):

        self.datasets = [

            "sample_dataset_1.csv",

            "sample_dataset_2.csv",

            "sample_dataset_3.csv",

            "sample_dataset_4.csv",

            "sample_dataset_5.csv"
        ]

        self.analysis_results = []


    # ======================================
    # LOAD DATASET
    # ======================================

    def load_all_datasets(self):

        loaded_data = []

        for dataset in self.datasets:

            data = load_dataset(
                dataset
            )

            loaded_data.append({

                "dataset_name":
                dataset,

                "data":
                data
            })

        return loaded_data


    # ======================================
    # COMPUTE DATASET METRICS
    # ======================================

    def compute_dataset_metrics(
        self,
        dataset_name,
        dataset
    ):

        preservation_scores = []

        decay_rates = []

        risk_levels = []

        total_archives = len(dataset)

        total_files = dataset[
            "InitialFiles"
        ].sum()

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

            risk = analyze_risk(
                decay_rate
            )

            preservation_scores.append(
                score
            )

            decay_rates.append(
                decay_rate
            )

            risk_levels.append(
                risk
            )

        average_preservation = round(

            np.mean(
                preservation_scores
            ),

            2
        )

        average_decay = round(

            np.mean(
                decay_rates
            ),

            3
        )

        critical_count = risk_levels.count(
            "Critical"
        )

        moderate_count = risk_levels.count(
            "Moderate"
        )

        low_count = risk_levels.count(
            "Low"
        )

        dataset_result = {

            "dataset_name":
            dataset_name,

            "total_archives":
            total_archives,

            "total_files":
            int(total_files),

            "average_preservation":
            average_preservation,

            "average_decay":
            average_decay,

            "critical_risk":
            critical_count,

            "moderate_risk":
            moderate_count,

            "low_risk":
            low_count
        }

        return dataset_result


    # ======================================
    # GENERATE COMPARATIVE REPORT
    # ======================================

    def generate_comparative_report(self):

        loaded_datasets = (
            self.load_all_datasets()
        )

        for dataset_object in loaded_datasets:

            dataset_name = dataset_object[
                "dataset_name"
            ]

            dataset = dataset_object[
                "data"
            ]

            result = self.compute_dataset_metrics(

                dataset_name,

                dataset
            )

            self.analysis_results.append(
                result
            )

        return pd.DataFrame(
            self.analysis_results
        )


    # ======================================
    # VISUALIZE COMPARATIVE ANALYSIS
    # ======================================

    def generate_visualizations(self):

        os.makedirs(
            "outputs",
            exist_ok=True
        )

        dataframe = pd.DataFrame(
            self.analysis_results
        )

        # ----------------------------------
        # PRESERVATION COMPARISON GRAPH
        # ----------------------------------

        plt.style.use(
            "dark_background"
        )

        plt.figure(
            figsize=(12, 6)
        )

        plt.bar(

            dataframe[
                "dataset_name"
            ],

            dataframe[
                "average_preservation"
            ]
        )

        plt.xlabel(
            "Datasets"
        )

        plt.ylabel(
            "Average Preservation Score"
        )

        plt.title(
            "Comparative Preservation Analysis"
        )

        plt.xticks(
            rotation=15
        )

        plt.tight_layout()

        plt.savefig(
            "outputs/comparative_preservation.png"
        )

        plt.close()

        # ----------------------------------
        # DECAY RATE ANALYSIS
        # ----------------------------------

        plt.figure(
            figsize=(12, 6)
        )

        plt.plot(

            dataframe[
                "dataset_name"
            ],

            dataframe[
                "average_decay"
            ],

            marker='o',

            linewidth=3
        )

        plt.title(
            "Average Decay Rate Comparison"
        )

        plt.xlabel(
            "Datasets"
        )

        plt.ylabel(
            "Decay Rate"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "outputs/decay_analysis.png"
        )

        plt.close()

        # ----------------------------------
        # RISK DISTRIBUTION GRAPH
        # ----------------------------------

        x = np.arange(
            len(
                dataframe[
                    "dataset_name"
                ]
            )
        )

        width = 0.25

        plt.figure(
            figsize=(14, 6)
        )

        plt.bar(

            x - width,

            dataframe[
                "critical_risk"
            ],

            width,

            label="Critical"
        )

        plt.bar(

            x,

            dataframe[
                "moderate_risk"
            ],

            width,

            label="Moderate"
        )

        plt.bar(

            x + width,

            dataframe[
                "low_risk"
            ],

            width,

            label="Low"
        )

        plt.xticks(

            x,

            dataframe[
                "dataset_name"
            ],

            rotation=10
        )

        plt.xlabel(
            "Datasets"
        )

        plt.ylabel(
            "Archive Count"
        )

        plt.title(
            "Risk Distribution Across Datasets"
        )

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            "outputs/risk_distribution.png"
        )

        plt.close()


    # ======================================
    # EXPORT ANALYSIS REPORT
    # ======================================

    def export_analysis_report(self):

        os.makedirs(
            "reports",
            exist_ok=True
        )

        report_path = (
            "reports/"
            "comparative_analysis_report.txt"
        )

        with open(
            report_path,
            "w"
        ) as file:

            file.write(
                "DIGITAL ARCHIVE "
                "COMPARATIVE ANALYSIS REPORT\n\n"
            )

            for result in self.analysis_results:

                file.write(

                    f"Dataset: "
                    f"{result['dataset_name']}\n"
                )

                file.write(

                    f"Total Archives: "
                    f"{result['total_archives']}\n"
                )

                file.write(

                    f"Total Files: "
                    f"{result['total_files']}\n"
                )

                file.write(

                    f"Average Preservation: "
                    f"{result['average_preservation']}%\n"
                )

                file.write(

                    f"Average Decay Rate: "
                    f"{result['average_decay']}\n"
                )

                file.write(

                    f"Critical Risk Archives: "
                    f"{result['critical_risk']}\n"
                )

                file.write(

                    f"Moderate Risk Archives: "
                    f"{result['moderate_risk']}\n"
                )

                file.write(

                    f"Low Risk Archives: "
                    f"{result['low_risk']}\n"
                )

                file.write(
                    "\n-----------------------\n\n"
                )

        return report_path


# ==========================================
# EXECUTION ENGINE
# ==========================================

if __name__ == "__main__":

    analysis_system = (
        ComparativeAnalysisSystem()
    )

    dataframe = (
        analysis_system
        .generate_comparative_report()
    )

    analysis_system.generate_visualizations()

    report_location = (
        analysis_system
        .export_analysis_report()
    )

    print(
        "\nCOMPARATIVE ANALYSIS COMPLETED\n"
    )

    print(dataframe)

    print(
        f"\nReport Exported To:"
        f" {report_location}"
    )