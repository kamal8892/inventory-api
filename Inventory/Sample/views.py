from .models import Euser,Category,Supplier,Product,Inventory
from django.contrib.auth.models import User
from rest_framework import status
from django.core.cache import cache
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import EuserSerializer,CategorySerializer,SupplierSerializer,ProductSerializer,InventorySerializer

CACHE_TTL = 300

@api_view(['POST'])
def signup(request):
    try:
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone = request.data.get('phone')
        email = request.data.get('email')
        gender = request.data.get('gender')
        password = request.data.get('password')
        age = request.data.get('age')

        if not first_name or not last_name  or not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        print(first_name, last_name, phone, email, gender, password)

        # Create the user
        euser = Euser.objects.create(
            # id=id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            gender=gender,
            age = age,
            password=make_password(password)
        )
        print("Euser created successfully")
        print(first_name, last_name, phone, email, gender, password)

        user = User.objects.create(  
            username=email,         
            first_name=first_name,
            last_name=last_name,
            email=email
            )
        user.set_password(password)
        user.save()
        print("User created successfully")
        # user.set_password(password)
        # user.save()
        print("My all data are done")
        print(first_name, last_name, phone, email, gender, password)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return JsonResponse({
            'refresh': str(refresh),
            'access': str(access_token),
            "success":"User created successfully done"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:  
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        euser = User.objects.get(email=email)  
    except User.DoesNotExist:
        return JsonResponse({'msg': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
    print("all done")
    if euser.check_password(password):  
        refresh = RefreshToken.for_user(euser)  
        access_token = refresh.access_token
        print("USer login successfully and token are created")

        return JsonResponse({
            'refresh': str(refresh),
            'access': str(access_token),
            "success": "Login successfully"
        }, status=status.HTTP_200_OK)

    return JsonResponse({'msg': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


# user update 

@api_view(['PUT'])
def UserUpdate(request):
    id = request.data.get('id')
    username = request.data.get('username')
    password = request.data.get('password')

    # Ensure the ID is provided
    if not id:
        return JsonResponse({'msg': 'User id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the user based on the provided ID
        euser = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'msg': 'User not found with the provided ID'}, status=status.HTTP_404_NOT_FOUND)

    # Update username and/or password only if provided
    if not username and not password:
        return JsonResponse({'msg': 'At least one field (username or password) is required to update'}, status=status.HTTP_400_BAD_REQUEST)

    if username:
        euser.username = username
    if password:
        euser.set_password(password)

    # Save the updated user details
    euser.save()
    
    refresh = RefreshToken.for_user(euser)
    access_token = refresh.access_token

    return JsonResponse({
        'msg': 'User updated successfully',
        'refresh': str(refresh),
        'access': str(access_token)
    }, status=status.HTTP_200_OK)




# category api

@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def category_api(request,pk=None):
    if request.method == 'GET':
        cat = Category.objects.all()
        serializer = CategorySerializer(cat ,many=True)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'Data Created successfully'},status=status.HTTP_201_CREATED)
        return JsonResponse({'msg':'all fields are required'},status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if pk is not None:
            try:
                category = Category.objects.get(id=pk)
            except Category.DoesNotExist:
                return JsonResponse({'msg':'id not found'},status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(category,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg':'category updated successfully'},status=status.HTTP_200_OK)
            return JsonResponse({'msg':'category id is required'},status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        if pk is not None:
            categ = Category.objects.get(id=pk)
            categ.delete()
            return JsonResponse({'msg':'category deleted successfully'},status=status.HTTP_200_OK)
        
def list(self, request, *args, **kwargs):
        cache_key = 'category_list'
        categories = cache.get(cache_key)
        if not categories:
            Login.debug("Cache miss for category list")
            categories = super().list(request, *args, **kwargs).data
            cache.set(cache_key, categories, CACHE_TTL)

        else:
            Login.debug("Cache hit for category list")

        return Response(categories)

# Supplier api

@api_view(['GET','POST','PUT','DELETE'])
def supplier_api(request,pk=None):
    if request.method == 'GET':
        supplier = Supplier.objects.all()
        serializer = SupplierSerializer(supplier,many = True)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'supplier data created successfully'},status=status.HTTP_201_CREATED)
        return JsonResponse({'msg':'supplier all fileds are required'},status=status.HTTP_400_BAD_REQUEST)
    

    elif request.method == 'PUT':
        if pk is not None:
            try:
                supplier = Supplier.objects.get(id=pk)
            except Supplier.DoesNotExist:
                return JsonResponse({'msg':'id not found'},status=status.HTTP_404_NOT_FOUND)
            serializer = SupplierSerializer(supplier,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg':'supplier updated successfully'},status=status.HTTP_200_OK)
            return JsonResponse({'msg':'supplier id is required'},status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        if pk is not None:
            supplier = supplier.objects.get(id=pk)
            supplier.delete()
            return JsonResponse({'msg':'supplier is deleted successfully'},status=status.HTTP_200_OK)
        
    
def list(self, request, *args, **kwargs):
        cache_key = 'category_list'
        categories = cache.get(cache_key)
        if not categories:
            Login.debug("Cache miss for category list")
            categories = super().list(request, *args, **kwargs).data
            cache.set(cache_key, categories, CACHE_TTL)

        else:
            Login.debug("Cache hit for category list")

        return Response(categories)  

# product api

@api_view(['GET','POST','PUT','DELETE'])
def product_api(request,pk=None):
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product,many=True)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'product created successfully'},status=status.HTTP_201_CREATED)
        return JsonResponse({'msg':'All fields are required'},status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if pk is not None:
            try:
                product = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                return JsonResponse({'msg':'product id not found so check your product id'},status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg':'product updated successfully'},status=status.HTTP_200_OK)
            return JsonResponse({'msg':'product id not correct'},status=status.HTTP_400_BAD_REQUEST)
        

    elif request.method == 'DELETE':
        if pk is not None:
            product = Product.objects.get(id=pk)
            product.delete()
            return JsonResponse({'msg':'product deleted successfully'},status=status.HTTP_200_OK)

def list(self, request, *args, **kwargs):
        cache_key = 'category_list'
        categories = cache.get(cache_key)
        if not categories:
            Login.debug("Cache miss for category list")
            categories = super().list(request, *args, **kwargs).data
            cache.set(cache_key, categories, CACHE_TTL)

        else:
            Login.debug("Cache hit for category list")

        return Response(categories)

# inventory api

@api_view(['GET','POST','PUT','DELETE'])
def inventory_api(request,pk=None):
    if request.method == 'GET':
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory,many=True)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'inventory created successfully'},status=status.HTTP_201_CREATED)
        return JsonResponse({'msg':'All fields are required'},status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if pk is not None:
            try:
                inventory = Inventory.objects.get(id=pk)
            except Inventory.DoesNotExist:
                return JsonResponse({'msg':'inventory id not found so check your product id'},status=status.HTTP_404_NOT_FOUND)
            serializer = InventorySerializer(inventory, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg':'inventory updated successfully'},status=status.HTTP_200_OK)
            return JsonResponse({'msg':'inventory id not correct'},status=status.HTTP_400_BAD_REQUEST)
        

    elif request.method == 'DELETE':
        if pk is not None:
            inventory = Inventory.objects.get(id=pk)
            inventory.delete()
            return JsonResponse({'msg':'inventory deleted successfully'},status=status.HTTP_200_OK)
def list(self, request, *args, **kwargs):
        cache_key = 'category_list'
        categories = cache.get(cache_key)
        if not categories:
            Login.debug("Cache miss for category list")
            categories = super().list(request, *args, **kwargs).data
            cache.set(cache_key, categories, CACHE_TTL)

        else:
            Login.debug("Cache hit for category list")

        return Response(categories)