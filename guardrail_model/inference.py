import torch
from transformers import DistilBertTokenizerFast
from transformers import DistilBertForSequenceClassification


class GuardrailClassifier:
    """
    DistilBERT based guardrail classifier used to detect:
    - valid queries
    - out_of_scope queries
    - jailbreak/prompt injection/adverserial attacks
    - PHI/PII request
    """

    def __init__(self, model_path: str):

        self.model_path = model_path

        self.label_map = {
            0: "VALID",
            1: "OUT_OF_SCOPE",
            2: "JAILBREAK_PI_ADV",
            3: "PHI_PII_FLAG"
        }

        self.device = self._get_device()

        self.tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)

        self.model = DistilBertForSequenceClassification.from_pretrained(
            model_path
        )

        self.model.to(self.device)

        self.model.eval()

    def _get_device(self):
        """
        Automatically select best available device.
        """

        if torch.cuda.is_available():
            return torch.device("cuda")

        if torch.backends.mps.is_available():
            return torch.device("mps")

        return torch.device("cpu")

    def classify(self, query: str):
        """
        Classify a query into one of the guardrail categories.

        Returns
        -------
        dict
            {
                "label": "VALID",
                "confidence": 0.94
            }
        """

        inputs = self.tokenizer(
            query,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256,
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():

            outputs = self.model(**inputs)

            logits = outputs.logits

            probs = torch.softmax(logits, dim=1)

            confidence, predicted_class = torch.max(probs, dim=1)

        label = self.label_map[predicted_class.item()]

        return {
            "label": label,
            "confidence": confidence.item(),
        }