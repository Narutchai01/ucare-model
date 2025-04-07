from cout_api import count_api
from reqcount import ImageObject, ResultObject


def acne_count(imageURL: str, cur) -> tuple:

    acnesDatas = []

    resultData = []

    nameAcneData = []

    whiteheadData = ImageObject(
        name="whitehead",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//Health-133.acne-001-5569be33e2174af18cc1513bdfa52610-2.jpeg",
        points=[[371, 165, 2, 392, 184, 3], [157, 113, 2, 180, 135, 3], [110, 216, 2, 132, 238, 3], [
            721, 317, 2, 739, 339, 3], [250, 211, 2, 272, 235, 3], [285, 164, 2, 307, 187, 3]]
    )

    acnesDatas.append(whiteheadData)

    blackheadData = ImageObject(
        name="blackhead",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//Blackheads-2-scaled.jpeg",
        points=[[1051, 592, 2, 1138, 692, 3], [920, 330, 2, 1007, 413, 3], [1465, 77, 2, 1539, 147, 3], [
            999, 1098, 2, 1095, 1177, 3], [994, 815, 2, 1068, 902, 3], [1522, 430, 2, 1605, 531, 3]]
    )

    acnesDatas.append(blackheadData)

    red_pimpleData = ImageObject(
        name="red pimple",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//S_0917_acne_M1080444.original.max-600x600.jpg",
        points=[[321, 186, 2, 332, 199, 3], [490, 312, 2, 505, 330, 3], [
            379, 99, 2, 393, 114, 3], [330, 57, 2, 348, 74, 3], [265, 166, 2, 280, 180, 3]]
    )

    acnesDatas.append(red_pimpleData)

    inflamedacneData = ImageObject(
        name="inflamed acne",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//p734-f3.jpg",
        points=[[331, 416, 2, 377, 464, 3], [411, 403, 2, 446, 438, 3],
                [597, 388, 2, 635, 435, 3], [543, 312, 2, 588, 357, 3]]
    )

    acnesDatas.append(inflamedacneData)

    pimple_with_pusData = ImageObject(
        name="pimple with pus",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//ct098011009_e_fig1.png",
        points=[[705, 555, 2, 763, 606, 3], [880, 546, 2, 921, 584, 3], [1027, 808, 2, 1066, 847, 3], [
            58, 729, 2, 113, 779, 3], [493, 235, 2, 529, 274, 3], [219, 476, 2, 277, 536, 3], [1066, 401, 2, 1116, 454, 3]]
    )
    acnesDatas.append(pimple_with_pusData)

    noduleData = ImageObject(
        name="nodule",
        path="https://qgxunldaghfxbofuvrdx.supabase.co/storage/v1/object/public/pathfinder//me3azeozzun71.jpg",
        points=[[321, 186, 2, 332, 199, 3], [490, 312, 2, 505, 330, 3], [
            379, 99, 2, 393, 114, 3], [330, 57, 2, 348, 74, 3], [265, 166, 2, 280, 180, 3]]
    )

    acnesDatas.append(noduleData)

    for data in acnesDatas:
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
                nameAcneData.append(data.name)
            else:
                continue

    return resultData, nameAcneData
