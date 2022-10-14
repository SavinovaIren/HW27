from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
import json

from HW27 import settings
from ads.models import Category, Ad, User, Location


def main(request):
    return JsonResponse({"status": "ok"})


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


@method_decorator(csrf_exempt, name="dispatch")
class AdsUpdateView(UpdateView):
    model = Ad
    fields = ['name', "author", "price", "description", "category", "is_published"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ads_data = json.loads(request.body)

        self.object.name = ads_data["name"]
        self.object.price = ads_data["price"]
        self.object.author = get_object_or_404(User, username=ads_data["author"])
        self.object.description = ads_data["description"]
        self.object.is_published = ads_data["is_published"]
        self.object.category = get_object_or_404(Category, name=ads_data["category"])

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author,
            "category": self.object.category,
            "price": self.object.price,
            "description": self.object.description,
            "image": self.object.image.url,
            "is_published": self.object.is_published

        }, safe=False, json_dumps_params={'ensure_ascii': False})


class AdsView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.order_by("-price")
        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)

        response = []
        for ad in page_obj:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "category": ad.category.name if ad.category.name else "Без категории",
                "price": ad.price,
                "description": ad.description,
                "image": ad.image.url,
                "is_published": ad.is_published
            })
        return JsonResponse({'ads': response, 'pages': page_obj.number, 'total': page_obj.paginator.count}, safe=False,
                            json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "category", "price", "description", "is_published"]

    def post(self, request, *args, **kwargs):
        ads_list = json.loads(request.body)
        author = get_object_or_404(User, username=ads_list['author'])
        category = get_object_or_404(Category, name=ads_list['category'])

        ads = Ad.objects.create(
            name=ads_list["name"],
            author=author,
            category=category,
            price=ads_list["price"],
            description=ads_list["description"],
            is_published=ads_list["is_published"] if 'is_published' in ads_list else False
        )

        return JsonResponse({"id": ads.id,
                             "name": ads.name,
                             "author": ads.author.username,
                             "category": ads.category.name,
                             "price": ads.price,
                             "description": ads.description,
                             "is_published": ads.is_published
                             }, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


class AdsDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        ads = self.get_object()
        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author": ads.author.username,
            "category": ads.category.name,
            "price": ads.price,
            "description": ads.description,
            "is_published": ads.is_published,
            "images": ads.image.url if ads.image else None
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list.order_by("username")
        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page = request.GET.get("page")
        page_obj = paginator.get_page(page)

        response = []
        for user in page_obj:
            response.append({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
            })
        return JsonResponse({'ads': response, 'pages': page_obj.number, 'total': page_obj.paginator.count}, safe=False,
                            json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'location']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.create(username=data['username'],
                                   password=data['password'],
                                   first_name=data['first_name'],
                                   last_name=data['last_name'],
                                   role=data['role'])
        for loc in data['location_id']:
            location = Location.objects.get_or_create(name=loc)
            user.location.add(location)
        return JsonResponse({'id': user.id,
                             'username': user.username,
                             'password': user.password,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'role': user.role,
                             'location': [str(u) for u in user.location.all()]},
                            safe=False, json_dumps_params={'ensure_ascii': False})
