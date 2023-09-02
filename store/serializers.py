from rest_framework import serializers
from .models import Product, Cart, CartItem
from accounts.models import CustomUser
import re

def contains_valid_characters(input_string):
    """
    Check if the input string contains only letters, numbers, and spaces, and is not empty.

    Parameters:
        input_string (str): The string to be validated.

    Returns:
        bool: True if the string contains only letters, numbers, and spaces,
              and is not empty (not consisting only of spaces). False otherwise.

    Examples:
        >>> contains_valid_characters("Hello123")
        True

        >>> contains_valid_characters("AbCdEfG")
        True

        >>> contains_valid_characters("123456789")
        True

        >>> contains_valid_characters("Hello, world!")
        False

        >>> contains_valid_characters("Spaces are allowed")
        True

        >>> contains_valid_characters("123#abc")
        False

        >>> contains_valid_characters("   ")
        False
    """    
    pattern = r'^[a-zA-Z0-9 ]+$'
    
    match = re.match(pattern, input_string)
    
    if not match or input_string.strip() == '':
        return False
    
    return True


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = ('id','name', 'price', 'description', 'stock')
        
        
    def validate_name(self, name):
        if len(name) <= 2:
            raise serializers.ValidationError('Name must be at least 3 characters long')
        elif not contains_valid_characters(name):
            raise serializers.ValidationError('Name cant have special characters')
        elif Product.objects.filter(name=name.capitalize()).exists():
            raise serializers.ValidationError("Name is already Taken")
        else:
            return name.capitalize()
        
    def validate_price(self,price):
        if price <= 0:
            raise serializers.ValidationError("Price must be higher than 0")
        return price
    
    def validate_description(self, description):
        if len(description) <= 2:
            raise serializers.ValidationError('Description must be at least 3 characters long')
        else:
            return description.capitalize()

    def validate_stock(self,stock):
        if stock <= 0:
            raise serializers.ValidationError("Stock cant be lower than 1")
        return stock

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product.id')

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

class CartIteReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')   
    


class CartReadSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cart_items = CartIteReadSerializer(many=True)
    user = serializers.EmailField(source='owner.email',read_only=True)
    class Meta:
        model = Cart
        fields = ('cart_items','total','user')
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['total'] = float(ret['total'])  # Convert the total to a Python float
        return ret
        
        
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    completed = serializers.BooleanField(read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ('cart_items','total','owner', 'completed')
        
    
    def validate_cart_items(self, cart_items):
        if len(cart_items) == 0:
            raise serializers.ValidationError("Cart must have at least one item")
        items = []
        for cart_item in cart_items:
            cart_id = cart_item.get('product').get('id')
            items.append(cart_id)
            if len(items) != len(set(items)):
                raise serializers.ValidationError("Cart cant have duplicate items")
            quantity = cart_item.get('quantity')
            product = cart_item.get('product').get('id')
            if product.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock. Only {product.stock} left")
            if quantity <=0:
                raise serializers.ValidationError("Quantity must be higher than 0")
        return cart_items
    
    def validate_owner(self, owner):
        cart = Cart.objects.filter(owner=owner)
        if cart.exists():
            for car in cart:
                if car.completed == False:
                    raise serializers.ValidationError("User already has a cart")
        return owner
        
    def create(self, validated_data):
        owner = validated_data.pop('owner')
        cart_items_data = validated_data.pop('cart_items')
        cart = Cart.objects.create(owner=owner)
        total = 0
        for cart_item_data in cart_items_data:
            product = cart_item_data['product']['id']
            product_id = product.id
            product = Product.objects.get(id=product_id)
            CartItem.objects.create(cart=cart, product=product, quantity=cart_item_data['quantity'])
            total+=product.price*cart_item_data['quantity']
        cart.total = total
        cart.save(update_fields=['total', 'owner'])
        return cart
    
    def update(self, instance, validated_data):
        cart_items_data = validated_data.pop('cart_items')
        total = 0
        for cart_item_data in cart_items_data:
            product = cart_item_data['product']['id']
            product_id = product.id
            product = Product.objects.get(id=product_id)
            CartItem.objects.filter(cart=instance, product=product).update(quantity=cart_item_data['quantity'])
            total+=product.price*cart_item_data['quantity']
        instance.total = total
        instance.save(update_fields=['total'])
        return instance
    # { "cart_items": [ {"product": 1, "quantity": 2}, {"product": 2, "quantity": 3} ] }
