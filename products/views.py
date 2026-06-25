from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from orders.models import OrderItem
from decimal import Decimal
from django.db.models import Q
from wishlist.models import Wishlist
from cart.models import CartItem
from recent.models import RecentlyViewed


from .models import (
    Category,
    Product
)

from .serializers import (
    CategorySerializer,
    ProductSerializer
)


class CategoryListAPIView(
    generics.ListAPIView
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(
    generics.ListAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "is_active",
    ]

    search_fields = [
    "name",
    "description",
    "sku",
    "category__name",
]
    ordering_fields = [
        "price",
        "created_at",
    ]

class ProductDetailAPIView(
    generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductSearchAPIView(generics.ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        keyword = self.request.GET.get("q")

        if keyword:
            return Product.objects.filter(
                name__icontains=keyword
            )

        return Product.objects.none()
class ProductRecommendationAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):

        product = Product.objects.filter(
            id=product_id,
            is_active=True
        ).first()

        if not product:
            return Response(
                {"error": "Product not found"},
                status=404
            )

        recommendations = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(
            id=product.id
        )[:5]

        serializer = ProductSerializer(
            recommendations,
            many=True
        )

        return Response({
            "current_product": product.name,
            "recommended_products": serializer.data
        })
class FeaturedProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        featured_products = Product.objects.filter(
            is_featured=True,
            is_active=True
        )

        serializer = ProductSerializer(
            featured_products,
            many=True
        )

        return Response(serializer.data)
class NewArrivalsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        new_products = Product.objects.filter(
            is_active=True
        ).order_by("-created_at")[:10]

        serializer = ProductSerializer(
            new_products,
            many=True
        )

        return Response(serializer.data)
class BestSellerProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        best_sellers = (
            Product.objects.filter(
                is_active=True
            )
            .annotate(
                total_orders=Count("orderitem")
            )
            .order_by("-total_orders")[:10]
        )

        serializer = ProductSerializer(
            best_sellers,
            many=True
        )

        return Response({
            "best_sellers": serializer.data
        })
class CustomersAlsoBoughtAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):

        # Get all orders containing the current product
        order_ids = OrderItem.objects.filter(
            product_id=product_id
        ).values_list(
            "order_id",
            flat=True
        )

        # Find other products from those orders
        products = Product.objects.filter(
            order_items__order_id__in=order_ids,
            is_active=True
        ).exclude(
            id=product_id
        ).annotate(
            purchase_count=Count("order_items")
        ).order_by(
            "-purchase_count"
        ).distinct()[:10]

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response({
            "customers_also_bought": serializer.data
        })
class SimilarPriceProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):

        product = Product.objects.filter(
            id=product_id,
            is_active=True
        ).first()

        if not product:
            return Response(
                {"error": "Product not found"},
                status=404
            )

        min_price = product.price * Decimal("0.80")
        max_price = product.price * Decimal("1.20")

        products = Product.objects.filter(
            price__gte=min_price,
            price__lte=max_price,
            is_active=True
        ).exclude(
            id=product.id
        )

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response({
            "current_product": product.name,
            "similar_price_products": serializer.data
        })
class PersonalizedRecommendationAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response(
                {"error": "user_id is required"},
                status=400
            )

        category_ids = set()

        # Wishlist
        for item in Wishlist.objects.filter(user_id=user_id):
            category_ids.add(item.product.category_id)

        # Cart
        for item in CartItem.objects.filter(cart__user_id=user_id):
            category_ids.add(item.product.category_id)

        # Orders
        for item in OrderItem.objects.filter(order__user_id=user_id):
            category_ids.add(item.product.category_id)

        # Recently Viewed
        for item in RecentlyViewed.objects.filter(user_id=user_id):
            category_ids.add(item.product.category_id)

        products = Product.objects.filter(
            category_id__in=category_ids,
            is_active=True
        ).distinct()[:10]

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response({
            "recommended_products": serializer.data
        })
class LowStockProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        low_stock_products = Product.objects.filter(
            stock__lte=10,
            is_active=True
        ).order_by("stock")

        serializer = ProductSerializer(
            low_stock_products,
            many=True
        )

        return Response({
            "low_stock_products": serializer.data
        })
class OutOfStockProductsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        out_of_stock_products = Product.objects.filter(
            stock=0,
            is_active=True
        )

        serializer = ProductSerializer(
            out_of_stock_products,
            many=True
        )

        return Response({
            "out_of_stock_products": serializer.data
        })
from django.db.models import Sum

class InventoryDashboardAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        total_products = Product.objects.count()

        in_stock_products = Product.objects.filter(
            stock__gt=0
        ).count()

        low_stock_products = Product.objects.filter(
            stock__gt=0,
            stock__lte=10
        ).count()

        out_of_stock_products = Product.objects.filter(
            stock=0
        ).count()

        total_inventory_quantity = Product.objects.aggregate(
            total=Sum("stock")
        )["total"] or 0

        total_inventory_value = 0

        for product in Product.objects.all():
            total_inventory_value += (
                product.price * product.stock
            )

        return Response({
            "total_products": total_products,
            "in_stock_products": in_stock_products,
            "low_stock_products": low_stock_products,
            "out_of_stock_products": out_of_stock_products,
            "total_inventory_quantity": total_inventory_quantity,
            "total_inventory_value": total_inventory_value
        })