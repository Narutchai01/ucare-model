from huggingface_hub import InferenceClient
import os


def classify_skin_type(image_url: str, cur):
    client = InferenceClient(
        provider=os.getenv("PROVIDER"),
        api_key=os.getenv("API_KEY"),
    )

    resultName = "skin"
    resultID = 0

    try:
        # Use the Hugging Face Inference API instead of local model
        output = client.image_classification(
            image_url, model="dima806/skin_types_image_detection"
        )

        # Process the results
        if output and len(output) > 0:
            # Get the top prediction
            top_prediction = output[0]
            predicted_class = top_prediction["label"]
            confidence = top_prediction["score"] * 100

            # Return normal if confidence is below 60%
            if confidence < 60:
                resultName = "normal"
            else:
                resultName = predicted_class
        else:
            resultName = "normal"  # Default if API returns no results
    except Exception as e:
        print(f"Model inference error: {e}")
        resultName = "normal"  # Default if model throws an error
        return f"{resultName} skin", 19  # Return early on error

    # Query the database to get the corresponding ID for the resultName

    resultName = f"{resultName} skin"
    cur.execute("SELECT id FROM face_problems WHERE name = %s", (resultName,))
    result = cur.fetchone()
    if result:
        resultID = result[0]
    else:
        resultID = 0

    return resultName, resultID
