from django.db import connection  # Django bazasiga ulanish uchun


def execute_sql(query, params=None):
    """
    Raw SQL so'rovlarini bajaruvchi universal funksiya.
    Natijalarni tuple emas, dictionary ko'rinishida qaytaradi.
    """
    try:
        with connection.cursor() as cursor:          # Cursor ochiladi
            cursor.execute(query, params)            # SQL so'rov bajariladi

            columns = [col[0] for col in cursor.description]  # Ustun nomlari olinadi

            rows = cursor.fetchall()                 # Barcha qatorlar olinadi

            # Har bir qatorni ustun nomlari bilan dict ga aylantiramiz
            return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"[SQL ERROR]: {e}")                   # Xatoni terminalga chiqaramiz
        return []                                    # Xato bo'lsa bo'sh list qaytaramiz
