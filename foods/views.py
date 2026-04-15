from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from common.utils import execute_sql

def is_ofitsiant_or_admin(user):
    return user.role in ['admin', 'waiter']

@api_view(['GET'])
@permission_classes([AllowAny])
def food_list(request):
    sql = """
        SELECT f.id, f.name, f.description, f.price, c.name as category_name 
        FROM foods_food f 
        JOIN foods_category c ON f.category_id = c.id;
    """
    data = execute_sql(sql)
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_food(request):
    if not is_ofitsiant_or_admin(request.user):
        return Response({"error": "Sizda taom qo'shish huquqi yo'q"}, status=403)
        
    data = request.data
    name = data.get('name')
    desc = data.get('description', '')
    price = data.get('price')
    category_id = data.get('category_id')
    
    if not (name and price and category_id):
        return Response({"error": "name, price va category_id kiritish shart."}, status=400)
        
    sql = """
        INSERT INTO foods_food (name, description, price, category_id) 
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    res = execute_sql(sql, [name, desc, price, category_id])
    
    if res:
        return Response({"message": "Taom muvaffaqiyatli qo'shildi", "food_id": res[0]['id']})
    return Response({"error": "Xatolik yuz berdi"}, status=500)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_food(request, pk):
    if not is_ofitsiant_or_admin(request.user):
        return Response({"error": "Ruxsat yo'q"}, status=403)
        
    data = request.data
    name = data.get('name')
    desc = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')
    
    sql = "UPDATE foods_food SET "
    fields = []
    params = []
    
    if name:
        fields.append("name = %s")
        params.append(name)
    if desc is not None:
        fields.append("description = %s")
        params.append(desc)
    if price:
        fields.append("price = %s")
        params.append(price)
    if category_id:
        fields.append("category_id = %s")
        params.append(category_id)
        
    if not fields:
        return Response({"error": "Ma'lumot jo'natilmadi."}, status=400)
        
    sql += ", ".join(fields) + " WHERE id = %s RETURNING id;"
    params.append(pk)
    
    res = execute_sql(sql, params)
    if res:
        return Response({"message": "Taom ma'lumotlari yangilandi"})
    return Response({"error": "Taom topilmadi."}, status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_food(request, pk):
    if not is_ofitsiant_or_admin(request.user):
        return Response({"error": "Ruxsat yo'q"}, status=403)
        
    sql = "DELETE FROM foods_food WHERE id = %s RETURNING id;"
    res = execute_sql(sql, [pk])
    
    if res:
        return Response({"message": "Taom o'chirildi"})
    return Response({"error": "Taom topilmadi."}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    if not is_ofitsiant_or_admin(request.user):
        return Response({"error": "Ruxsat yo'q"}, status=403)
    
    name = request.data.get('name')
    if not name:
        return Response({"error": "name maydoni to'ldirilsin"}, status=400)
        
    sql = "INSERT INTO foods_category (name) VALUES (%s) RETURNING id;"
    res = execute_sql(sql, [name])
    return Response({"message": "Yangi kategoriya yaratildi", "id": res[0]['id']})
