from django.template.defaultfilters import title
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from django.db import transaction
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer, CategoryValidateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductValidateSerializer,
    ReviewListSerializer, ReviewDetailSerializer, ReviewValidateSerializer
)


# ===== CATEGORY =====

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategoryListSerializer(categories, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        name = serializer.validated_data.get('name')
        with transaction.atomic():
            category = Category.objects.create(
                name=name,
            )
            category.save()
        return Response(
                 status=status.HTTP_201_CREATED,
                 data=CategoryDetailSerializer(category).data)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(CategoryDetailSerializer(category).data)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        category.name = request.data.get('name')
        category.save()

        return Response(
            status=status.HTTP_200_OK,
            data=CategoryDetailSerializer(category).data
        )


# ===== CATEGORY COUNT =====

@api_view(['GET'])
def category_with_count_api_view(request):
    categories = Category.objects.annotate(
        products_count=Count('products')
    )
    data = CategoryListSerializer(categories, many=True).data
    return Response(data=data)


# ===== PRODUCT =====

@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializer(products, many=True).data
        return Response(data=data)


    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category = serializer.validated_data.get('category')

        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description = description,
                price = price,
                category = category,
            )
            product.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ProductDetailSerializer(product).data)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data
        )


# ===== PRODUCT REVIEWS =====

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.prefetch_related('reviews').annotate(
        rating=Avg('reviews__stars')
    )

    data = ProductDetailSerializer(products, many=True).data
    return Response(data=data)


# ===== REVIEW =====

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewListSerializer(reviews, many=True).data
        return Response(data=data)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        print(request.data)
        print(serializer.validated_data)

        text=serializer.validated_data.get('text')
        stars=serializer.validated_data.get('stars')
        product_id=serializer.validated_data.get('product_id')

        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                stars=stars,
                product_id=product_id
            )
            review.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewDetailSerializer(review).data
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ReviewDetailSerializer(review).data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')
        review.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewDetailSerializer(review).data
        )