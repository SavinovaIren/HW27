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


class AdsUpdateSerialiser(serializers.Serializer):
    author = serializers.SlugRelatedField(required=False, queryset=User.objects.all(),
                                            slug_field='author')
    category = serializers.SlugRelatedField(required=False, queryset=Category.objects.all(),
                                            slug_field='category')
    class Meta:
        model = Ad
        fields = ['name', "author", "price", "description", "category", "is_published"]

    def is_valid(self, *, raise_exception=False):
        self._author = self.initial_data.pop('author')
        self._category = self.initial_data.pop('category')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        ad = super().save(**kwargs)
        for auth in self._author:
            author, _ = Ad.objects.get_or_create(name=auth)
            ad.author.add(author)
        for cat in self._category:
            category, _ = Ad.objects.get_or_create(name=cat)
            ad.author.add(category)
        return ad



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
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

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
