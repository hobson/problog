import pandas as pd

def create_csv(data):
    labels = ["conversationId", "username", "bot_response", "user_response", "classification"]
    formattedData = {label: [] for label in labels}
    for row in data:
        for i, label in enumerate(labels):
            formattedData[label].append(row[i])
    df = pd.DataFrame(formattedData)
    df.to_csv("data.csv", index=False)