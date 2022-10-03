from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
import json

from ads.models import Category, Ads


def main(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class CatView(View):
    def get(self, request):
        categories = Category.objects.all()

        search_cat = request.GET.get("name", None)
        if search_cat:
            categories = categories.filter(name=search_cat)

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        cat_list = json.loads(request.body)

        cat = Category.objects.create(name=cat_list["name"])

        return JsonResponse({"id": cat.id,
                             "name": cat.name}, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()

        search_ads = request.GET.get("name", None)
        if search_ads:
            ads = ads.filter(name=search_ads)

        response = []
        for ad in ads:
            response.append({
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
            })
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        ads_list = json.loads(request.body)

        ads = Ads.objects.create(
            name=ads_list["name"],
            author=ads_list["author"],
            price=ads_list["price"],
            description=ads_list["name"],
            address=ads_list["name"],
            is_published=ads_list["is_published"]
        )

        return JsonResponse({
            "id": ads.pk,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published
        })


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
            "author": ads.author,
            "price": ads.price,
        }, safe=False, json_dumps_params={'ensure_ascii': False})
