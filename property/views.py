import datetime
from django.db.models import Avg, Q, F, Min, Max
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework import pagination


import json

from rest_framework.views import APIView

from .models import Property, PropertyRoom, PropertyImage, RoomBed, Facility, PeriodPrice
from .serializer import PropertySerializer, PropertyRoomSerializer, RoomBedSerializer, PropertyImageSerializer,\
    FacilitySerializer, PeriodPriceSerializer

# from accounts.models import User
# import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/reservations')
from reservations.models import Reservation
from comments.models import PropertyComment
from rest_framework.permissions import BasePermission


class IsPropertyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user


# Create your views here.
class ViewProperty(RetrieveAPIView):
    # Every one can view the property
    permission_classes = [AllowAny]
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # Get the serializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        facilities = instance.facility_set.all()
        serialized_data['facilities'] = FacilitySerializer(facilities, many=True).data

        # Get average rating
        serialized_data['rating'] = instance.get_average_rating()
        # comments = PropertyComment.objects.filter(under=instance)
        # if comments.exists():
        #     avg_rating = comments.aggregate(Avg('rating'))
        #     serialized_data['rating'] = avg_rating['rating__avg']
        # else:
        #     serialized_data['rating'] = None

        # xs = PropertyRoom.objects.all()
        # for x in xs:
        #     print(x.property.id)

        # Get latest price
        serialized_data['price'] = instance.get_latest_price()
        # latest_price = PeriodPrice.objects.filter(property__id=instance.id).order_by('-start_date').first()
        # if latest_price:
        #     serialized_data['price'] = latest_price.price
        # else:
        #     print("No price find")
        #     serialized_data['price'] = None

        # Add Room and bed information
        # rooms = instance.room_set.all()
        # serialized_data['rooms'] = []

        # for room in rooms:
        #     serialized_room = PropertyRoomSerializer(room).data
        #     beds = RoomBed.objects.filter(room=room)
        #     serialized_beds = RoomBedSerializer(beds, many=True).data
        #     serialized_room['beds'] = serialized_beds
        #     serialized_data['rooms'].append(serialized_room)

        # images = instance.image_set.all()
        # serialized_data['images'] = []
        # for image in images:
        #     serialized_image = PropertyImageSerializer(image).data
        #     serialized_data['images'].append(serialized_image)
        images = instance.image_set.all()
        serialized_data['images'] = PropertyImageSerializer(images, many=True).data

        return Response(serialized_data)


class CreateProperty(CreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        # Deserialize the main property data and save the instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        property_instance = serializer.save(owner=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #
        # # Deserialize and save the nested facilities, images, and rooms
        # facilities_data = request.data.get('facilities', [])
        # images_data = request.data.get('images', [])
        # rooms_data = request.data.get('rooms', [])

        # for facility_data in facilities_data:
        #     print("Create facility")
        #     Facility.objects.create(property=property_instance, **facility_data)

        # for image_data in images_data:
        #     print("Create Image")
        #     PropertyImage.objects.create(property=property_instance, **image_data)

        # for room_data in rooms_data:
        #     print("create Room")
        #     room_serializer = PropertyRoomSerializer(data=room_data)
        #     if room_serializer.is_valid():
        #         room_instance = room_serializer.save(property=property_instance)
        #         for bed_data in room_data.get('beds', []):
        #             RoomBed.objects.create(room=room_instance, **bed_data)
        #     else:
        #         return Response(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # # Extract the price from the input data and create a PeriodPrice instance
        # price = request.data.get('price')
        # if price is not None:
        #     try:
        #         price = float(price)
        #         if price >= 0:
        #             print("Fetching Price")
        #             PeriodPrice.objects.create(property=property_instance, price=price,
        #                                        start_date=datetime.date.today())
        #         else:
        #             return Response({"price": "Price must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)
        #     except ValueError:
        #         return Response({"price": "Price must be a valid float."}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"price": "Price field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Return the created property instance
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddFacility(CreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.kwargs['property_id']
        property_instance = Property.objects.get(id=property_id)

        if self.request.user != property_instance.owner:
            raise NotAuthenticated("You are not the owner of this property.")

        serializer.save(property=property_instance)


class FacilityListAPIView(ListAPIView):
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        return Facility.objects.filter(property_id=property_id)


class FacilityUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated, IsPropertyOwner]


class AddPropertyImageView(CreateAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.kwargs['property_id']
        property_instance = Property.objects.get(id=property_id)

        if self.request.user != property_instance.owner:
            raise NotAuthenticated("You are not the owner of this property.")

        serializer.save(property=property_instance)


class PropertyImagesListAPIView(ListAPIView):
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        return PropertyImage.objects.filter(property_id=property_id)


class PropertyImageUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsAuthenticated, IsPropertyOwner]


class AddPropertyPeriodicPriceView(CreateAPIView):
    queryset = PeriodPrice.objects.all()
    serializer_class = PeriodPriceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.kwargs['property_id']
        property_instance = Property.objects.get(id=property_id)

        if self.request.user != property_instance.owner:
            raise NotAuthenticated("You are not the owner of this property.")

        serializer.save(property=property_instance)


class PeriodPricesListAPIView(ListAPIView):
    serializer_class = PeriodPriceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        return PeriodPrice.objects.filter(property_id=property_id)


class PeriodicPriceUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PeriodPrice.objects.all()
    serializer_class = PeriodPriceSerializer
    permission_classes = [IsAuthenticated, IsPropertyOwner]


class AllPropertyView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        sort = self.request.query_params.get('sort', '-price')
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)

        if start and end:
            start_date = parse_date(start)
            end_date = parse_date(end)
        else:
            start_date = None
            end_date = None

        latest_prices = PeriodPrice.objects.annotate(max_start_date=Max('start_date')).filter(start_date=F('max_start_date'))

        queryset = Property.objects.annotate(latest_price=F('price_set__price')).filter(price_set__in=latest_prices)

        if start_date and end_date:
            available_properties = [property for property in queryset if property.is_available(start_date, end_date)]
            queryset = Property.objects.filter(id__in=[p.id for p in available_properties])

        if sort == 'price':
            queryset = queryset.order_by('latest_price')
        elif sort == '-price':
            queryset = queryset.order_by('-latest_price')
        elif sort == 'capacity':
            queryset = queryset.order_by('capacity')

        return queryset


class UpdatePropertyView(RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    # permission_classes = [IsAuthenticated, IsPropertyOwner]


# class UpdatePropertyView(UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PropertySerializer
#     queryset = Property.objects.all()
#
#     def get_object(self):
#         property_instance = super().get_object()
#         curr_user = self.request.user
#         property_owner = property_instance.owner
#
#         if curr_user != property_owner:
#             raise NotAuthenticated("401 Not Authenticated.")
#         return property_instance
#
#     def update(self, request, *args, **kwargs):
#         property_instance = self.get_object()
#         serializer = self.get_serializer(property_instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#
#         # Update the main property data
#         self.perform_update(serializer)
#
#         # Update the nested facilities, images, and rooms
#         facilities_data = request.data.get('facilities', [])
#         images_data = request.data.get('images', [])
#         rooms_data = request.data.get('rooms', [])
#         price = request.data.get('price', None)
#
#         # Update facilities
#         property_instance.facility_set.all().delete()
#         for facility_data in facilities_data:
#             Facility.objects.create(property=property_instance, **facility_data)
#
#         # Update images
#         property_instance.image_set.all().delete()
#         for image_data in images_data:
#             PropertyImage.objects.create(property=property_instance, **image_data)
#
#         # Update rooms
#         property_instance.room_set.all().delete()
#         for room_data in rooms_data:
#             room_serializer = PropertyRoomSerializer(data=room_data)
#             if room_serializer.is_valid():
#                 room_instance = room_serializer.save(property=property_instance)
#                 for bed_data in room_data.get('beds', []):
#                     RoomBed.objects.create(room=room_instance, **bed_data)
#             else:
#                 return Response(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         # Update price
#         if price is not None:
#             start_date = datetime.date.today()
#             PeriodPrice.objects.create(Property=property_instance, price=price, start_date=start_date)
#
#         return Response(serializer.data)


class DeletePropertyView(DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        property_instance = super().get_object()
        curr_user = self.request.user
        property_owner = property_instance.owner

        if curr_user != property_owner:
            raise NotAuthenticated("401 Not Authenticated.")
        return property_instance


class FilterView(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        queryset = Property.objects.all()
        location = self.request.data.get('location')
        owner = self.request.data.get('owner')
        description = self.request.data.get('description')
        name = self.request.data.get('name')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if owner:
            queryset = queryset.filter(owner__icontains=owner)
        if description:
            queryset = queryset.filter(description__icontains=description)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


# class SortByView(ListAPIView):
#     serializer_class = PropertySerializer
#     permission_classes = [AllowAny]
#     pagination_class = pagination.PageNumberPagination
#
#     def get_queryset(self):
#         order = self.request.query_params.get('order', 'price')
#
#         if order == 'rating':
#             # Calculate the average rating for each property
#             property_ratings = Property.objects.annotate(
#                 avg_rating=Avg('propertyComment_set__rating')
#             ).order_by('-avg_rating')
#             return property_ratings
#
#         # By default, sort by price
#         properties_with_lowest_price = Property.objects.annotate(
#             min_price=Min('price_set__price')
#         ).order_by('min_price')
#         return properties_with_lowest_price


class SortByWithAvailabilityView(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        order = self.request.query_params.get('order', 'price')

        if not start_date or not end_date:
            return Property.objects.none()

        # Find properties with overlapping reservations
        overlapping_reservations = Reservation.objects.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date),
            status__in=['pending', 'ongoing', 'ready'],
        )

        # Exclude properties with overlapping reservations
        available_properties = Property.objects.exclude(
            id__in=overlapping_reservations.values('property')
        )

        # Sort the properties by the specified order
        if order == 'rating':
            sorted_properties = available_properties.annotate(
                avg_rating=F('propertycomment_set__rating')
            ).order_by('-avg_rating')
        else:  # Default to sorting by 'price'
            sorted_properties = available_properties.order_by('price')

        return sorted_properties


class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, pk, format=None):
        image_file = request.FILES.get('image')
        image_name = request.data.get('name', '')

        if not image_file:
            return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            property_instance = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

        PropertyImage.objects.create(property=property_instance, name=image_name, image=image_file)

        return Response({"success": "Image uploaded and associated with property"}, status=status.HTTP_201_CREATED)


# class UploadMultipleImagesView(APIView):
#     parser_classes = [MultiPartParser]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, pk, format=None):
#         property_instance = get_object_or_404(Property, pk=pk)
#         images_data = self.request.FILES.getlist('images')
#
#         if not images_data:
#             return Response({"detail": "No images provided."}, status=status.HTTP_400_BAD_REQUEST)
#
#         for image_data in images_data:
#             PropertyImage.objects.create(property=property_instance, image=image_data)
#
#         return Response({"detail": "Images uploaded successfully."}, status=status.HTTP_201_CREATED)


class DeleteImageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, property_pk, image_pk, *args, **kwargs):
        property_instance = get_object_or_404(Property, pk=property_pk)
        image_instance = get_object_or_404(PropertyImage, pk=image_pk, property=property_instance)

        # Check if the user has permission to delete the image
        if request.user == property_instance.owner or request.user.is_staff:
            image_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this image."},
                            status=status.HTTP_403_FORBIDDEN)


class PropertyPriceView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PeriodPriceSerializer

    def get_queryset(self):
        property_id = self.kwargs['pk']
        prices_instance = Property.objects.get(id=property_id).price_set.all()
        return prices_instance



# class FilterByView(ListAPIView):
#     serializer_class = PropertySerializer
#     permission_classes = [AllowAny]
#     pagination_class = pagination.PageNumberPagination
#
#     def get_queryset(self):
#         location = self.request.query_params.get('location', None)
#         available_dates = self.request.query_params.get('available_dates', None)
#         capacity = self.request.query_params.get('capacity', None)
#         facility = self.request.query_params.get('facility', None)
#
#         collection = Property.objects.all()
#         if location:
#             return Property.objects.filter(location=location)
#         if capacity:
#             return Property.objects.filter(capacity=capacity)
#         if facility:
#             res = Property.objects.none()
#             fa = Facility.objects.filter(name=facility)
#             for f in fa:
#                 res = res.union(Property.objects.filter(id=f.property.id))
#
#             return res
#         if available_dates:




