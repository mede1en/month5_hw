from rest_framework import serializers
from .models import Category, Product, Review


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price category'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text product stars'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



#hw4
class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=255)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255)
    description = serializers.CharField(required=True, min_length=2, max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # хотела спросить вместо форинкей используем лист как на классном

    def validate_category(self, category):
        if not Category.objects.filter(id=category.id).exists():
            raise serializers.ValidationError('Category does not exist!')
        return category

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=2, max_length=255)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    stars = serializers.IntegerField(min_value=1, max_value=5)

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value