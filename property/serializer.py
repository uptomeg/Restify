from rest_framework.serializers import ModelSerializer
# import sys

# sys.path.insert(1, '/group_2256/P2/restify/p2/property')
from property.models import Property, Facility, PropertyImage, PropertyRoom, RoomBed, PeriodPrice

#
# class PropertySerializer(ModelSerializer):
#     class Meta:
#         model = Property
#         fields = '__all__'
#         read_only_fields = ('owner', )


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class PropertyImageSerializer(ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['name', 'image']
        # model = PropertyImage
        # fields = ('id', 'name', 'image')
        # extra_kwargs = {
        #     'image': {'required': False},
        # }


class RoomBedSerializer(ModelSerializer):
    class Meta:
        model = RoomBed
        fields = '__all__'


class PropertyRoomSerializer(ModelSerializer):
    beds = RoomBedSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = PropertyRoom
        fields = '__all__'


class PropertySerializer(ModelSerializer):
    # facilities = FacilitySerializer(many=True, required=False, read_only=True)
    # images = PropertyImageSerializer(many=True, required=False, read_only=True)
    # rooms = PropertyRoomSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('owner',)


# class PeriodPriceSerializer(ModelSerializer):
#     class Meta:
#         model = PeriodPrice
#         fields = '__all__'
#         read_only_fields = ('property', )


class PeriodPriceSerializer(ModelSerializer):
    class Meta:
        model = PeriodPrice
        fields = ['price', 'start_date']


