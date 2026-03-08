import requests
import pandas as pd
from tqdm import tqdm

API_URL = "http://localhost:8000/analyze"

def run_eval():

    df = pd.read_csv("benchmark_dataset_queries.csv")

    results = []
    errors = 0
    for _, row in tqdm(df.iterrows(), total=len(df)):
        query = row["query"]
        label = row["label"]
        print(f"Running query: {query} | Label: {label}")
        response = requests.post(
            API_URL,
            json={"query": query}
        )
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            errors += 1
            output = response.text
        else:
            output = response.json()["response"]

        results.append({
                "query": query,
                "label": label,
                "response": output
            })

        pd.DataFrame(results).to_csv(
                "system_outputs.csv",
                index=False
            )
    
    print(f"Evaluation complete with {errors} errors. Results saved to system_outputs.csv")

if __name__ == "__main__":
    run_eval()