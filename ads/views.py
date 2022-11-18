from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from HW27 import settings
from ads.models import Category, Ad, Location, Selection, User
from ads.permissions import IsOwnerOrStuff, IsOwnerOrStuffAd
from ads.serializers import UserListSerializer, UserCreateSerializer, LocationSerializer, AdListSerializer, \
    UserUpdateSerializer, UserDeleteSerializer, UserSerializer, AdsDeleteSerializer, CategoryDeleteSerializer, \
    AdDetailSerializer, SelectionListSerializer, SelectionUpdateSerializer, SelectionCreateSerializer, \
    SelectionDetailSerializer, SelectionDeleteSerializer, AdsUpdateSerialiser, AdsCreateSerializer


def main(request):
    return JsonResponse({"status": "ok"})

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class CategoryView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_cat = request.GET.get("name", None)
        if search_cat:
            self.object_list = self.object_list.filter(name=search_cat)
        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_list = json.loads(request.body)

        cat = Category.objects.create(name=cat_list["name"])

        return JsonResponse({"id": cat.id,
                             "name": cat.name}, safe=False,
                            json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse({"id": self.object.id,
                             "name": self.object.name,
                             "author_id_id": self.object.author_id_id,
                             "price": self.object.price,
                             "description": self.object.description,
                             "image": self.object.image.url,
                             "is_published": self.object.is_published
                             }, safe=False, json_dumps_params={'ensure_ascii': False})




class AdsUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdsUpdateSerialiser
    permission_classes = [IsOwnerOrStuffAd]



class AdsView(ListAPIView):
    queryset = Ad.objects.order_by("-price").all()
    serializer_class = AdListSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat", None)
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("text", None)
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location", None)
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        price_to = request.GET.get("price_to")

        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)


        return super().get(self, *args, **kwargs)


class AdsCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdsCreateSerializer
#class AdsCreateView(CreateView):
    # model = Ad
    # fields = ["name", "author", "category", "price", "description", "is_published"]
    #
    # def post(self, request, *args, **kwargs):
    #     ads_list = json.loads(request.body)
    #     author = get_object_or_404(User, username=ads_list['author'])
    #     category = get_object_or_404(Category, name=ads_list['category'])
    #
    #     ads = Ad.objects.create(
    #         name=ads_list["name"],
    #         author=author,
    #         category=category,
    #         price=ads_list["price"],
    #         description=ads_list["description"],
    #         is_published=ads_list["is_published"] if 'is_published' in ads_list else False
    #     )
    #
    #     return JsonResponse({"id": ads.id,
    #                          "name": ads.name,
    #                          "author": ads.author.username,
    #                          "category": ads.category.name,
    #                          "price": ads.price,
    #                          "description": ads.description,
    #                          "is_published": ads.is_published
    #                          }, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})


class AdsDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated]


class CategoryDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CategoryDeleteSerializer



class AdsDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdsDeleteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuffAd]



class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuff]


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuff]



class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuff]




class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer

class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuff]

class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]

class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer
    permission_classes = [IsAuthenticated]

class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDeleteSerializer
    permission_classes = [IsAuthenticated]

