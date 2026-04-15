import math
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from common.utils import execute_sql

REST_LAT = 41.2995
REST_LON = 69.2401

def oradagi_masofa(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    data = request.data
    user_id = request.user.id
    
    lat = float(data.get('latitude', 0))
    lon = float(data.get('longitude', 0))
    
    items = data.get('items', []) 
    
    if not items:
        return Response({"error": "Taom tanlanmagan"}, status=400)
    
    umumiy_soni = sum(int(item.get('quantity', 1)) for item in items)
    
    masofa_km = oradagi_masofa(REST_LAT, REST_LON, lat, lon)
    
    yol_vaqti = math.ceil(masofa_km) * 3
    pishish_vaqti = math.ceil(umumiy_soni / 4) * 5
    
    jami_vaqt = yol_vaqti + pishish_vaqti
    
    order_sql = """
        INSERT INTO orders_order (customer_id, status, latitude, longitude, delivery_time, created_at) 
        VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING id;
    """
    
    order_res = execute_sql(order_sql, [user_id, 'PENDING', lat, lon, jami_vaqt])
    order_id = order_res[0]['id']
    
    for item in items:
        item_sql = """
            INSERT INTO orders_orderitem (order_id, food_id, quantity) 
            VALUES (%s, %s, %s) RETURNING id;
        """
        execute_sql(item_sql, [order_id, item.get('food_id'), item.get('quantity')])
        
    return Response({
        "message": "Buyurtma qabul qilindi",
        "order_id": order_id,
        "bizgacha_masofa_km": round(masofa_km, 2),
        "taxminiy_yetkazib_berish_vaqti": f"{jami_vaqt} minut"
    })

def is_ofitsiant_or_admin(user):
    return user.role in ['admin', 'waiter']

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    if not is_ofitsiant_or_admin(request.user):
        return Response({"error": "Ruxsat yo'q"}, status=403)
        
    order_sql = """
        SELECT o.id, o.status, o.delivery_time, o.created_at, u.username as mijoz
        FROM orders_order o
        JOIN users_user u ON o.customer_id = u.id
        ORDER BY o.created_at DESC;
    """
    orders = execute_sql(order_sql)
    
    for order in orders:
        item_sql = """
            SELECT f.name, i.quantity 
            FROM orders_orderitem i
            JOIN foods_food f ON i.food_id = f.id
            WHERE i.order_id = %s;
        """
        order['ichidagi_taomlar'] = execute_sql(item_sql, [order['id']])
        
    return Response(orders)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk):
    if not is_ofitsiant_or_admin(request.user):
        return Response({"error": "Ruxsat yo'q"}, status=403)
        
    yangi_status = request.data.get('status')
    if not yangi_status:
        return Response({"error": "Status kiritilmadi"}, status=400)
        
    sql = "UPDATE orders_order SET status = %s WHERE id = %s RETURNING id, status;"
    res = execute_sql(sql, [yangi_status, pk])
    
    if res:
        return Response({
            "message": f"Buyurtma (# {pk}) statusi o'zgardi: {res[0]['status']}"
        })
    return Response({"error": "Topilmadi!"}, status=404)
