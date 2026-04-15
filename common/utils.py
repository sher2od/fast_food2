from django.db import connection # bazaga ulanish


def execute_sql(query, params=None):
    try:
        with connection.cursor() as cursor:          #  ochiladi 
            cursor.execute(query, params)            # SQL so'rov bajariladi

            columns = [col[0] for col in cursor.description]  # Ustun nomlari olinadi

            rows = cursor.fetchall()                 # xamma qator olinadi

            # xar bir qatorni dictga aylantiramiz
            return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"[SQL ERROR]: {e}")                  
        return []                                    
