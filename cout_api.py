from reqcount import ImageObject
from gradio_client import Client, handle_file


def count_api(imageURL: str, dataOBJ: ImageObject):
    try:
        client = Client("https://nikigoli-countgd.hf.space/")
        result = client.predict(
            image=handle_file(imageURL),
            text=dataOBJ.name,
            prompts={"image": handle_file(
                dataOBJ.path), "points": dataOBJ.points},
            api_name="/count_main"
        )

        return result[1]['value']
    except Exception as e:
        # Log the error or handle it based on your application's needs
        print(f"Error occurred in count_api: {str(e)}")
        return {"error": "Failed to process the image. Please try again later."}
