    
from database.database import create_connection, run_sql
from utilities.prompting import CHAT_RETRIEVE_QUERY
import json

import json


def upload_chat_in_db(chat_data):
    query = "INSERT INTO history (chat) VALUES (%s) RETURNING id;"
    
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (json.dumps(chat_data),))
                row = cursor.fetchone()
                conn.commit()
                
                if row:
                    return {"message": "uploaded successfully", "id": row['id']}
                else:
                    return {"message": "Insert failed", "id": None}
                    
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error uploading chat:", e)
        return {"message": f"Upload failed: {str(e)}", "id": None}

def retrieve_chat_in_db():
    try: 

        conn = create_connection()
        result = run_sql(conn=conn,sql= CHAT_RETRIEVE_QUERY)
        conn.close()
        return [dict(res) for res in result]
    except Exception as e:
        return {
            "db_fetch_error":str(e)
        }