from fastapi import FastAPI
from db import get_db_connection
from pydantic import BaseModel
from count_facial import facial_count
from countance import acne_count
from skinanalysis import classify_skin_type
from skincare_recommand import get_skincare_recommendations, update_skincare_embeddings


app = FastAPI()


class Data(BaseModel):
    id: int
    image: str


@app.get("/")
async def root():
    update_skincare_embeddings()
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(data: Data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        image_url = data.image
        user_id = data.id
        nameAcne = []
        nameFacial = []

        # Find user in the database
        user_query = "SELECT * FROM users WHERE id = %s"
        cur.execute(user_query, (user_id,))
        user = cur.fetchone()

        if not user:
            return {"error": "User not found"}

        try:
            resultAcne = acne_count(image_url, cur)
            nameAcne = resultAcne[1]
        except Exception as e:
            # Graceful handling of acne_count failure
            print(f"Error in acne_count: {str(e)}")
            resultAcne = [None, []]
            nameAcne = []

        try:
            resultFacial = facial_count(image_url, cur)
            nameFacial = resultFacial[1]
        except Exception as e:
            # Graceful handling of facial_count failure
            print(f"Error in facial_count: {str(e)}")
            resultFacial = [None, []]
            nameFacial = []

        try:
            skin_type = classify_skin_type(image_url, cur)
        except Exception as e:
            # Graceful handling of skin type classification failure
            print(f"Error in classify_skin_type: {str(e)}")
            skin_type = [None, None]

        # Only attempt recommendations if we have necessary data
        skincare_id = []
        if nameAcne or nameFacial or skin_type[0]:
            try:
                skincare_id = get_skincare_recommendations(
                    f"{nameAcne}, {nameFacial}, {skin_type[0]}", cur, topk=5)
            except Exception as e:
                print(f"Error in get_skincare_recommendations: {str(e)}")

        return {
            "image": data.image,
            "user_id": data.id,
            "acne_type": resultAcne[0],
            "facial_type": resultFacial[0],
            "skin_id": skin_type[1],
            "skincare_id": skincare_id,
        }
    except Exception as e:
        # Global error handler
        print(f"Global error in predict endpoint: {str(e)}")
        return {"error": "An error occurred processing your request"}
    finally:
        # Always close cursor and connection
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
