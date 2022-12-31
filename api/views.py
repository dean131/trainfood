import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import *


@api_view(['POST'])
def product_list_view(request):
    data = json.loads(request.body)
    # Required [product_type]
    product_type = data['product_type'].lower()
    products = models.Product.objects.filter(product_type=product_type)
    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response({'status': 'success', 'data': serializer.data})


@api_view(['GET'])
def recomended_product_view(request):
    try:
        products = models.Product.objects.filter(is_recomended=True)
        product_serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response({
            'status': 'success',
            'data': product_serializer.data
        })
    except:
        print('===== Tidak ada product recomended ====')
    return Response({
        'status': 'failed',
        'message': "Tidak ada product recomended"
    })


@api_view(['POST'])
def update_item_view(request):
    data = json.loads(request.body)
    # Required [action, product_id, user_id]
    action = data['action']
    product_id = data['product_id']
    user_id = data['user_id']
    try:
        user = models.User.objects.get(id=user_id)
        product = models.Product.objects.get(id=product_id)
        order, created = models.Order.objects.get_or_create(user=user, is_checked_out=False)
        order_item, created = models.OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            order_item.quantity = (order_item.quantity + 1)
        elif action == 'remove':
            order_item.quantity = (order_item.quantity - 1)

        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
            order_item.quantity = 0
        order_serializer = OrderSerializer(order)
        return Response({
            'status': 'success',
            'data': {
                'item_quantity': order_item.quantity,
                'data_order': order_serializer.data
            }
        })
    except:
        print('=== order tidak ditemukan ==')
    return Response({
        'status': 'failed'
    })


@api_view(['POST'])
def cart_view(request):
    data = json.loads(request.body)
    # Required [user_id]
    user_id = data['user_id']
    try:
        user = models.User.objects.get(id=user_id)
        order = models.Order.objects.get(user=user, is_checked_out=False)
        order_items = order.orderitem_set.all()
        order_items_serializer = OrderItemSerializer(order_items, many=True, context={'request': request})
        order_serializer = OrderSerializer(order)
        return Response({
            'status': 'success',
            'data': {
                'order_item': order_items_serializer.data,
                'data_order': order_serializer.data}})
    except:
        print('===== Order Tidak Diutemukan =====')
    return Response({'status': 'failed'})

@api_view(['POST'])
def order_view(request):
    data = json.loads(request.body)
    # Required [user_id, seat_number, carriage_code]
    user_id = data['user_id']
    seat_number = data['seat_number']
    carriage_code = data['carriage_code']
    try:
        user = models.User.objects.get(id=user_id)
        order = models.Order.objects.get(user=user, is_checked_out=False)

        models.Address.objects.create(user=user, order=order, seat_number=seat_number, carriage_code=carriage_code)

        order.is_checked_out = True
        order.save()
        return Response({'status': 'success'})
    except:
        print('===== order_view (Gagal) =====')
    return Response({'status': 'failed'})

@api_view(['POST'])
def my_order_view(request):
    data = json.loads(request.body)
    user_id = data['user_id']
    try:
        user = models.User.objects.get(id=user_id)
        orders = models.Order.objects.filter(user=user, is_checked_out=True, is_complete=False)
        order_items = []
        for i in range(len(orders)):
            order_item = orders[i].orderitem_set.all()
            for j in range(len(order_item)):
                order_items.append(order_item[j])
        order_item_serializer = OrderItemSerializer(order_items, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'data': order_item_serializer.data
            })
    except:
        print('===== my_order_view (Gagal) =====')
    return Response({'status': 'failed'})


@api_view(['POST'])
def my_order_history_view(request):
    data = json.loads(request.body)
    user_id = data['user_id']
    try:
        user = models.User.objects.get(id=user_id)
        orders = models.Order.objects.filter(user=user, is_checked_out=True, is_complete=True)
        order_items = []
        for i in range(len(orders)):
            order_item = orders[i].orderitem_set.all()
            for j in range(len(order_item)):
                order_items.append(order_item[j])
        order_item_serializer = OrderItemSerializer(order_items, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'data': order_item_serializer.data
            })
    except:
        print('===== my_order_history_view (Gagal) =====')
    return Response({'status': 'failed'})