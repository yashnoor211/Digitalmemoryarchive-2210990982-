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
# RECOMMENDATION ENGINE
# ==========================================

class ArchiveRecommendationSystem:


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

        self.recommendation_results = []

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
    # GENERATE RECOMMENDATIONS
    # ======================================

    def generate_recommendation(
        self,
        risk_level,
        preservation_score,
        storage_condition,
        backup_status
    ):

        recommendations = []

        # ----------------------------------
        # RISK LEVEL RECOMMENDATIONS
        # ----------------------------------

        if risk_level == "Critical":

            recommendations.append(
                "Immediate archive backup required"
            )

            recommendations.append(
                "Migrate archives to secure storage"
            )

        elif risk_level == "Moderate":

            recommendations.append(
                "Periodic preservation monitoring advised"
            )

            recommendations.append(
                "Increase access verification frequency"
            )

        else:

            recommendations.append(
                "Archive condition currently stable"
            )

        # ----------------------------------
        # PRESERVATION SCORE LOGIC
        # ----------------------------------

        if preservation_score < 40:

            recommendations.append(
                "Deploy emergency preservation strategy"
            )

        elif preservation_score < 70:

            recommendations.append(
                "Optimize long-term retention policies"
            )

        else:

            recommendations.append(
                "Preservation performance acceptable"
            )

        # ----------------------------------
        # STORAGE CONDITION LOGIC
        # ----------------------------------

        if storage_condition == "Poor":

            recommendations.append(
                "Upgrade storage infrastructure"
            )

        elif storage_condition == "Medium":

            recommendations.append(
                "Perform periodic storage maintenance"
            )

        # ----------------------------------
        # BACKUP STATUS LOGIC
        # ----------------------------------

        if backup_status == "No":

            recommendations.append(
                "Enable automated cloud backup"
            )

        else:

            recommendations.append(
                "Backup redundancy successfully maintained"
            )

        return recommendations


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
        # DECAY ANALYSIS
        # ----------------------------------

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

        archive_score = preservation_score(

            initial_files,

            final_retention
        )

        archive_risk = analyze_risk(
            decay_rate
        )

        recommendations = (

            self.generate_recommendation(

                archive_risk,

                archive_score,

                storage_condition,

                backup_status
            )
        )

        return {

            "dataset_name":
            dataset_name,

            "archive_id":
            archive_id,

            "file_type":
            file_type,

            "preservation_score":
            archive_score,

            "risk_level":
            archive_risk,

            "recommendations":
            recommendations
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

                result = (
                    self.process_archive(

                        dataset_name,

                        row
                    )
                )

                self.recommendation_results.append(
                    result
                )

        return pd.DataFrame(
            self.recommendation_results
        )


    # ======================================
    # GENERATE VISUAL ANALYTICS
    # ======================================

    def generate_visualizations(self):

        dataframe = pd.DataFrame(
            self.recommendation_results
        )

        plt.style.use(
            "dark_background"
        )

        # ----------------------------------
        # RISK LEVEL DISTRIBUTION
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

            autopct="%1.1f%%"
        )

        plt.title(
            "Recommendation Risk Distribution"
        )

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"recommendation_risk_distribution.png"
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
            "Recommendation Performance by File Type"
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
            f"recommendation_filetype_analysis.png"
        )

        plt.close()


        # ----------------------------------
        # HEATMAP ANALYSIS
        # ----------------------------------

        heatmap_data = dataframe.pivot_table(

            values="preservation_score",

            index="file_type",

            columns="risk_level",

            aggfunc=np.mean
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
            "Recommendation Heatmap Analysis"
        )

        plt.tight_layout()

        plt.savefig(

            f"{self.output_directory}/"
            f"recommendation_heatmap.png"
        )

        plt.close()


    # ======================================
    # EXPORT RECOMMENDATION REPORT
    # ======================================

    def export_recommendation_report(self):

        report_path = (

            f"{self.output_directory}/"
            f"recommendation_report.txt"
        )

        with open(
            report_path,
            "w"
        ) as file:

            file.write(
                "DIGITAL ARCHIVE "
                "RECOMMENDATION REPORT\n\n"
            )

            file.write(

                f"Generated On: "
                f"{datetime.now()}\n\n"
            )

            for result in self.recommendation_results:

                file.write(

                    f"Dataset: "
                    f"{result['dataset_name']}\n"
                )

                file.write(

                    f"Archive ID: "
                    f"{result['archive_id']}\n"
                )

                file.write(

                    f"File Type: "
                    f"{result['file_type']}\n"
                )

                file.write(

                    f"Preservation Score: "
                    f"{result['preservation_score']}%\n"
                )

                file.write(

                    f"Risk Level: "
                    f"{result['risk_level']}\n"
                )

                file.write(
                    "Recommendations:\n"
                )

                for recommendation in result[
                    "recommendations"
                ]:

                    file.write(

                        f" - "
                        f"{recommendation}\n"
                    )

                file.write(
                    "\n=====================================\n\n"
                )

        return report_path


# ==========================================
# MAIN EXECUTION ENGINE
# ==========================================

if __name__ == "__main__":

    recommendation_engine = (
        ArchiveRecommendationSystem()
    )

    recommendation_dataframe = (

        recommendation_engine
        .process_all_datasets()
    )

    recommendation_engine.generate_visualizations()

    report_location = (

        recommendation_engine
        .export_recommendation_report()
    )

    print(
        "\nRECOMMENDATION ENGINE COMPLETED\n"
    )

    print(
        recommendation_dataframe.head()
    )

    print(
        f"\nRecommendation Report Saved At:"
        f" {report_location}"
    )