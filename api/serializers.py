from rest_framework import serializers
from restaurants.models import Restaurant
from django.contrib.auth.models import User
from restaurants.models import Item

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'name',
            'description',
            'price',
        ]

class RestaurantListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'opening_time',
            'closing_time',
            'detail',
            'update',
            'delete',
            ]


class RestaurantDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    items_list = serializers.SerializerMethodField()

    update = serializers.HyperlinkedIdentityField(
        view_name = "api-update",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )
    delete = serializers.HyperlinkedIdentityField(
        view_name = "api-delete",
        lookup_field = "id",
        lookup_url_kwarg = "restaurant_id"
        )


    def get_items_list (self, obj):
        list = Item.objects.filter(restaurant=obj)
        return ItemSerializer(list, many=True).data # you have to add .data otherwise you got unserializable error
                                                    # have to add many=True so that it accepts receiving multiple items

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'opening_time',
            'closing_time',
            'update',
            'delete',
            'items_list'
            ]

class RestaurantCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'description',
            'opening_time',
            'closing_time',
            ]