from django.urls import path
from .views import *

app_name = "property"
urlpatterns = [
    path('view/<int:pk>/', ViewProperty.as_view(), name='retrieveProperty'),
    path('create/', CreateProperty.as_view(), name='createPropertyInstance'),
    path('all/', AllPropertyView.as_view(), name='allPropertyInstance'),
    path('update/<int:pk>/', UpdatePropertyView.as_view(), name='updatePropertyInstance'),
    path('delete/<int:pk>/', UpdatePropertyView.as_view(), name='deletePropertyInstance'),

    path('upload-image/<int:property_id>/', AddPropertyImageView.as_view(), name='upload_image'),
    path('update-image/<int:pk>/', PropertyImageUpdateAPIView.as_view(), name='update_image'),
    path('delete-image/int:property_id>/', DeleteImageView.as_view(), name='delete_image'),

    path('add-facility/<int:property_id>/', AddFacility.as_view(), name='add_facility'),
    path('update-facility/<int:pk>/', FacilityUpdateAPIView.as_view(), name='update_facility'),

    path('add-price/<int:pk>/', AddPropertyPeriodicPriceView.as_view(), name='add_price'),
    path('update-price/<int:pk>/', PeriodicPriceUpdateAPIView.as_view(), name='update_price'),

    path('properties/<int:property_id>/images/', PropertyImagesListAPIView.as_view(), name='property_images'),
    path('properties/<int:property_id>/facilities/', FacilityListAPIView.as_view(), name='property_facilities'),
    path('properties/<int:property_id>/prices/', PeriodPricesListAPIView.as_view(), name='period_prices'),
]
