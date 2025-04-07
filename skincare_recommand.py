
from sentence_transformers import SentenceTransformer
import pandas as pd
from db import get_db_connection

embedder = SentenceTransformer('all-MiniLM-L6-v2')


def encode(content: str):
    return embedder.encode(content).tolist()


def get_skincare_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM skincares")

    # Fetch all records
    skincare_records = cur.fetchall()

    # Get column names from cursor description
    column_names = [desc[0] for desc in cur.description]

    # Create DataFrame from the records
    skincare_df = pd.DataFrame(skincare_records, columns=column_names)

    return skincare_df


def update_skincare_embeddings(content_column='description'):
    skincare_df = get_skincare_data()
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the content column exists
    if content_column not in skincare_df.columns:
        raise ValueError(
            f"Column '{content_column}' not found in skincare data")

    # Count of updated records
    update_count = 0

    # Process each record
    for _, row in skincare_df.iterrows():
        skincare_id = row['id']
        content = row[content_column]
        current_embedding = row.get('embedding')

        # Skip if content is None or empty
        if not content or pd.isna(content):
            continue

        # Only update if embedding is None or empty
        if current_embedding is None or pd.isna(current_embedding):
            # Generate embedding for the content
            embedding = encode(content)

            # Update the database with the new embedding
            cur.execute(
                "UPDATE skincares SET embedding = %s WHERE id = %s",
                (embedding, skincare_id)
            )

            update_count += 1

    # Commit the changes
    from db import conn
    conn.commit()

    return update_count


def get_skincare_recommendations(prolems: str, cur, topk: int = 5):

    embedding_problems = encode(prolems)

    query_embedding = '[' + ', '.join(map(str, embedding_problems)) + ']'

    sql_query = """ SELECT id ,embedding <=> %s ::vector AS similarity_score FROM skincares WHERE (embedding IS NOT NULL) LIMIT %s;"""

    cur.execute(sql_query, (query_embedding, topk))
    results = cur.fetchall()
    cur.close()

    skincares_id = [result[0] for result in results]

    return skincares_id
