import pandas as pd
import random
import nlpaug.augmenter.word as naw

df = pd.read_csv("data/guardrail_dataset_base.csv", delimiter="|")

paraphraser = naw.SynonymAug(aug_src='wordnet')
augmented_rows = []

for _, row in df.iterrows():

    text = row["QUERY"]
    label = row["LABEL"]

    # Original example
    augmented_rows.append((text,label))

    # Generate 3 paraphrases
    for _ in range(3):

        try:
            aug_text = paraphraser.augment(text)
            if isinstance(aug_text,list):
                aug_text = aug_text[0]

            augmented_rows.append((aug_text,label))

        except:
            pass


aug_df = pd.DataFrame(augmented_rows,columns=["QUERY","LABEL"])

print("Original size:",len(df))
print("Augmented size:",len(aug_df))

aug_df.to_csv("data/guardrail_dataset_augmented.csv",index=False)