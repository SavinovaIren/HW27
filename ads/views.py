from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
import json

from ads.models import Category, Ads


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

        cat = Category.objects.create(name=cat_list["name"], )

        return JsonResponse({"id": cat.id,
                             "name": cat.name, }, safe=False,
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
    model = Ads
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "image": self.object.image.url,
            "is_published": self.object.is_published,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', "author", "price", "description", "address", "is_published"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ads_data = json.loads(request.body)

        self.object.name = ads_data["name"]
        self.object.author_id = ads_data["author_id"]
        self.object.price = ads_data["price"]
        self.object.description = ads_data["description"]
        self.object.image = ads_data["image"]
        self.object.is_published = ads_data["is_published"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "image": self.object.image,
            "is_published": self.object.is_published,

        }, safe=False, json_dumps_params={'ensure_ascii': False})


class AdsView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        search_ads = request.GET.get("name", None)
        if search_ads:
            self.object_list = self.object_list.filter(name=search_ads)

        response = []
        for ad in self.object_list:
            response.append({
                "id": self.object_list.id,
                "name": self.object_list.name,
                "author_id": self.object_list.author_id,
                "price": self.object_list.price,
                "description": self.object_list.description,
                "image": self.object_list.image,
                "is_published": self.object_list.is_published,
            })
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ["name", "author", "price", "description", "address", "is_published"]

    def post(self, request, *args, **kwargs):
        ads_list = json.loads(request.body)

        ads = Ads.objects.create(
            name=ads_list["name"],
            author_id=ads_list["author_id"],
            price=ads_list["price"],
            description=ads_list["description"],
            image=ads_list["image"],
            is_published=ads_list["is_published"],
        )

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    def get(self, request, pk):
        cat = get_object_or_404(Category, id=pk)
        return JsonResponse({
            "id": cat.id,
            "name": cat.name,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


class AdsDetailView(DetailView):
    def get(self, request, pk):
        ads = get_object_or_404(Ads, id=pk)
        return JsonResponse({
            "id": ads.pk,
            "name": ads.name,
            "author_id": ads.author_id,
            "price": ads.price,
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
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
