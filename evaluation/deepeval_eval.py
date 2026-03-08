import pandas as pd
import time

from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import AnswerRelevancyMetric, TaskCompletionMetric
from deepeval.evaluate import evaluate

from evaluation.groq_judge import GroqJudgeLLM
from config.config import Config


DELAY = 40


judge_model = GroqJudgeLLM(
    api_key=Config.GROQ_API_KEY,
    model=Config.JUDGE_MODEL_NAME or "llama-3.3-70b-versatile"
)

# correctness_metric = GEval(
#     name="Correctness",
#     criteria="Determine whether the answer correctly performs the requested health dataset analysis.",
#     evaluation_params=[
#         LLMTestCaseParams.INPUT,
#         LLMTestCaseParams.ACTUAL_OUTPUT
#     ],
#     model=judge_model,
#     async_mode=False
# )

metrics = [
    AnswerRelevancyMetric(model=judge_model, async_mode=False),
    TaskCompletionMetric(model=judge_model, async_mode=False)
]

def remove_disclaimer(text):

    disclaimer_phrase = Config.disclaimer_phrase

    if disclaimer_phrase in text:
        return text.split(disclaimer_phrase)[-1]

    return text

df = pd.read_csv("evaluation/system_outputs.csv")

results = []


for idx, row in df.iterrows():

    print(f"Evaluating query {idx+1}/{len(df)}")

    clean_response = remove_disclaimer(row["response"])

    test_case = LLMTestCase(
        input=row["query"],
        actual_output=clean_response
    )

    eval_result = evaluate(
        test_cases=[test_case],
        metrics=metrics
    )

    # Extract metric results
    metric_results = eval_result.test_results[0].metrics_data

    row_result = {
        "query": row["query"],
        "response": row["response"]
    }

    for metric in metric_results:

        row_result[f"{metric.name}_score"] = metric.score
        row_result[f"{metric.name}_reason"] = metric.reason

    results.append(row_result)

    # Rate limiter
    time.sleep(DELAY)


# -----------------------------
# Save results
# -----------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "evaluation/deepeval_results.csv",
    index=False
)

print("Evaluation complete. Results saved.")