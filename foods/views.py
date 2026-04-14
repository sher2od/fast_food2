from django.http import JsonResponse
from common.utils import execute_sql

def food_list(request):
    sql = """
        SELECT f.id, f.name, f.description, f.price, c.name as category_name 
        FROM foods_food f 
        JOIN foods_category c ON f.category_id = c.id;
    """
    
    data = execute_sql(sql)
    
    return JsonResponse(data, safe=False)
