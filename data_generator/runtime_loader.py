import pandas as pd
from pathlib import Path
from semantic.semantic_service import SchemaSemanticService


class RuntimeDatasetLoader:

    def __init__(self):

        self.registry = SchemaSemanticService().fetch_schema()
        self.cache = {}

    def read_excel_file(self, file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, engine="openpyxl")
        df.columns = df.columns.str.strip()
        df.columns = [col.lower() for col in df.columns]
        return df

    def load_dataset(self, table_name: str):

        if table_name in self.cache:
            return self.cache[table_name]

        tables = self.registry.get("tables", {})

        if table_name not in tables:
            raise ValueError(f"Dataset {table_name} not found in schema")

        table_meta = tables[table_name]

        path = table_meta.get("path")

        if not path:
            raise ValueError(f"No dataset path defined for {table_name}")

        dataset_path = Path(path)

        df = self.read_excel_file(dataset_path)

        self.cache[table_name] = df

        return df


loader = RuntimeDatasetLoader()