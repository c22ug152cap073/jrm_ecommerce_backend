from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/v1/auth/",
        include("accounts.urls")
    ),

    path(
        "api/v1/products/",
        include("products.urls")
    ),

    path(
        "api/v1/cart/",
        include("cart.urls")
    ),

    path("api/v1/orders/", include("orders.urls")),
    path("api/v1/banners/", include("banners.urls")),
    path(
    "api/v1/reviews/",
    include("reviews.urls")),
    path(
    "api/v1/contact/",
    include("contact.urls")),
    path(
    "api/v1/returns/",
    include("returns.urls")),
    path(
    "api/v1/newsletter/",
    include("newsletter.urls")
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
