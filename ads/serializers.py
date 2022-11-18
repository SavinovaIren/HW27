from rest_framework import serializers

from ads.models import User, Location, Category, Ad, Selection


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    # не отображает локации
    location = serializers.SlugRelatedField(many=True,
                                            read_only=True,
                                            slug_field='name')

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, queryset=Location.objects.all(),
                                            many=True, slug_field='name')

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for loc in self._location:
            location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location)

        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, queryset=Location.objects.all(),
                                            many=True, slug_field='name')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for loc in self._location:
            location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location)

        return user


class AdsUpdateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"




class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(read_only=True,
                                            many=True, slug_field='name')

    class Meta:
        model = User
        fields = '__all__'


class AdsDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']


class CategoryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id']


class AdDetailSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    # category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = "__all__"


class SelectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class AdsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"