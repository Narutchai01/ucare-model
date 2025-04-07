from cout_api import count_api
from reqcount import ImageObject, ResultObject

import psycopg2 as pg


def facial_count(imageURL: str, cur):

    facialdata = []
    resultData = []
    nameFacialData = []

    black_red_markData = ImageObject(
        name="black and red mark",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//4847-residual_scar-1296x728-slide6_20200308155454.jpg",
        points=[[534, 294, 2, 587, 349, 3], [601, 234, 2, 654, 285, 3], [607, 298, 2, 647, 345, 3], [
            461, 581, 2, 514, 634, 3], [322, 404, 2, 360, 457, 3], [472, 201, 2, 506, 241, 3], [799, 276, 2, 854, 336, 3]]
    )

    facialdata.append(black_red_markData)

    freckles_and_dark_spotsData = ImageObject(
        name="freckles and dark spots",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//freckles-1.JPG",
        points=[[231, 153, 2, 509, 451, 3], [
            538, 67, 2, 678, 183, 3], [811, 58, 2, 991, 256, 3]]
    )

    facialdata.append(freckles_and_dark_spotsData)

    dull_skinData = ImageObject(
        name="dull facial skin",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//Tired-or-Dull-Looking-Skin-clinics.jpg",
        points=[[44, 290, 2, 279, 456, 3]]
    )

    facialdata.append(dull_skinData)

    enlarged_poresData = ImageObject(
        name="enlarged pores",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//1.jpg",
        points=[[112, 3, 2, 416, 293, 3]]
    )

    facialdata.append(enlarged_poresData)

    scarsData = ImageObject(
        name="scars",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//2568-04-04_23.32.35.png",
        points=[[470, 151, 2, 522, 215, 3], [323, 198, 2, 397, 268, 3], [431, 596, 2, 487, 660, 3], [221, 470, 2, 309, 538, 3], [
            274, 328, 2, 359, 397, 3], [346, 527, 2, 425, 593, 3], [174, 519, 2, 237, 571, 3], [249, 605, 2, 293, 654, 3], [470, 492, 2, 509, 549, 3]]
    )

    facialdata.append(scarsData)

    winklesData = ImageObject(
        name="wrinkles",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//59958684-portrait-of-an-elderly-woman-closeup-view-toned.jpg",
        points=[[341, 142, 2, 378, 189, 3], [280, 184, 2, 371, 263, 3], [7, 173, 2, 87, 277, 3], [
            6, 89, 2, 90, 164, 3], [7, 22, 2, 80, 76, 3], [163, 120, 2, 207, 189, 3], [301, 1, 2, 376, 98, 3]]
    )

    facialdata.append(winklesData)

    for data in facialdata:
        result = count_api(imageURL, data)
        if result == 0:
            continue
        else:
            # find data.name in the database
            cur.execute(
                "SELECT * FROM face_problems WHERE name = %s LIMIT 1", (data.name,))
            problem_data = cur.fetchone()
            if problem_data:
                # Get the id from the tuple using index position (assuming id is the first column)
                resultData.append(ResultObject(
                    problem_data[0], result).to_dict())
                nameFacialData.append(data.name)
            else:
                continue

    return resultData, nameFacialData
