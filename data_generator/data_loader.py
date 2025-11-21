import pandas as pd
import numpy as np
from config.config import Config
from logger import get_logger

logger = get_logger(__name__)

class DataManager:
    def __init__(self,data_path1: str = None, data_path2: str = None):
        self.df_health = pd.read_csv(data_path1) if data_path1 else None
        self.df_activity = pd.read_csv(data_path2) if data_path2 else None
        if self.df_health is None or self.df_activity is None:
            self._generate_mock_data()

    def _generate_mock_data(self):
        logger.info("Starting synthetic data generation...")
        np.random.seed(42)
        n_patients = 2000
        
        #dataset1
        self.df_health = pd.DataFrame({
            'Patient_Number': range(1, n_patients + 1),
            'Blood_Pressure_Abnormality': np.random.choice([0, 1], n_patients, p=[0.8, 0.2]), # 0=Normal, 1=Abnormal 
            'Level_of_Hemoglobin': np.round(np.random.normal(14, 2, n_patients), 1),
            'Genetic_Pedigree_Coefficient': np.random.uniform(0, 1, n_patients), # 0 to 1 scale [cite: 37]
            'Age': np.random.randint(18, 90, n_patients),
            'BMI': np.round(np.random.normal(25, 5, n_patients), 1),
            'Sex': np.random.choice([0, 1], n_patients), # 0=Male, 1=Female 
            'Pregnancy': np.zeros(n_patients),
            'Smoking': np.random.choice([0, 1], n_patients),
            'salt_content_in_the_diet': np.random.randint(1000, 5000, n_patients),
            'alcohol_consumption_per_day': np.random.randint(0, 500, n_patients),
            'Level_of_Stress': np.random.choice([1, 2, 3], n_patients), # 1=Low, 2=Normal, 3=High 
            'Chronic_kidney_disease': np.random.choice([0, 1], n_patients, p=[0.9, 0.1]),
            'Adrenal_and_thyroid_disorders': np.random.choice([0, 1], n_patients, p=[0.9, 0.1])
        })
        
        # Logic Fixes (Males cannot be pregnant)
        self.df_health.loc[self.df_health['Sex'] == 0, 'Pregnancy'] = 0
        self.df_health.loc[(self.df_health['Sex'] == 1) & (np.random.rand(n_patients) > 0.95), 'Pregnancy'] = 1

        logger.info(f"Generated Health Data: {n_patients} rows")
        
       #dataset2
        records = []
        for pid in range(1, n_patients + 1):
            is_sick = self.df_health.loc[self.df_health['Patient_Number'] == pid, 'Chronic_kidney_disease'].values[0]
            base = 3000 if is_sick else 7000
            for d in range(1, 11):
                steps = int(np.random.normal(base, 1500))
                records.append([pid, d, max(0, steps)])
                
        self.df_activity = pd.DataFrame(records, columns=['Patient_Number', 'Day_Number', 'Physical_activity'])

        logger.info(f"Generated Activity Data: {len(records)} rows")

    def get_schema_context(self) -> str:
        schema = """
        DATASET 1: df_health (One row per patient)
        - Patient_Number: (int) Unique ID
        - Blood_Pressure_Abnormality: (int) 0 = Normal, 1 = Abnormal
        - Level_of_Hemoglobin: (float) g/dl
        - Genetic_Pedigree_Coefficient: (float) 0 to 1 (0=Distant, 1=Immediate family history)
        - Age: (int) Years
        - BMI: (float) Body Mass Index
        - Sex: (int) 0 = Male, 1 = Female
        - Pregnancy: (int) 0 = No, 1 = Yes
        - Smoking: (int) 0 = No, 1 = Yes
        - salt_content_in_the_diet: (int) mg/day
        - alcohol_consumption_per_day: (int) ml/day
        - Level_of_Stress: (int) 1=Low, 2=Normal, 3=High (Ordinal)
        - Chronic_kidney_disease: (int) 0 = No, 1 = Yes
        - Adrenal_and_thyroid_disorders: (int) 0 = No, 1 = Yes

        DATASET 2: df_activity (Longitudinal - Multiple rows per patient)
        - Patient_Number: (int) Foreign Key
        - Day_Number: (int) 1 to 10
        - Physical_activity: (int) Steps per day in last 10 days
        """
        return schema

data_manager = DataManager(Config.dataset_path1, Config.dataset_path2)