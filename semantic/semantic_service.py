import yaml
from pathlib import Path


class SchemaSemanticRegistry:

    def __init__(self, path="config/data_schema.yaml"):
        self.path = Path(path)
        self.registry = self._load()

    def _load(self):
        with open(self.path, "r") as f:
            return yaml.safe_load(f)

    def get_tables(self):
        return self.registry.get("tables", {})

    def get_table(self, table_name):
        return self.registry.get("tables", {}).get(table_name, {})

    def get_columns(self, table_name):
        return self.get_table(table_name).get("columns", {})

    def get_column_metadata(self, table_name, column):
        return self.get_columns(table_name).get(column, {})

    def get_relationships(self):
        return self.registry.get("relationships", [])

class SchemaSemanticService:

    def __init__(self):
        self.registry = SchemaSemanticRegistry()

    def fetch_schema(self):
        return self.registry.registry