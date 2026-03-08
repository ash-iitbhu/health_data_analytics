def build_semantic_prompt(registry: dict) -> str:

    context = "DATA FRAME SCHEMA & SEMANTIC RULES:\n\n"

    for table_name, table_data in registry["tables"].items():
        context += f"\nTable: {table_name}\n"
        context += f"Description: {table_data.get('description','')}\n"
        context += f"Primary Key: {table_data.get('primary_key')}\n"
        context += "Columns:\n"

        for col, meta in table_data["columns"].items():
            level = meta.get("measurement_level", "unknown")
            entry = f"  - {col} ({level})"
            if "value_labels" in meta:
                labels = ", ".join(
                    [f"{k}={v}" for k, v in meta["value_labels"].items()]
                )

                entry += f" values[{labels}]"
            context += entry + "\n"

    context += "\nRelationships:\n"
    for rel in registry["relationships"]:
        context += (
            f"- {rel['left_table']}.{rel['left_key']} "
            f"= {rel['right_table']}.{rel['right_key']}\n"
        )

    return context