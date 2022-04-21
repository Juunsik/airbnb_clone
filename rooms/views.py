from django.views.generic import ListView, DetailView

# from django.http import Http404
# from django.urls import reverse
from django_countries import countries
from django.shortcuts import render
from . import models


# ======================================================================
# Class Based View 사용(3번째 방법)
# core.urls.py urlpatterns path : HomeView.as_view()
# templates/rooms/room_list.html 파일 필요
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # from django.utils import timezone //now 출력
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context


# ----------------------------------------------------------

# django paginator 사용(2번째 방법)
# core.urls.py urlpatterns path 일치해야 함
# templates/rooms/home.html 파일 필요
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(
#         room_list, 10, orphans=5
#     )  # orphans: 나머지, orphans보다 적게 남은 object를 마지막 이전 페이지에 추가로 출력

#     try:
#         rooms = paginator.page(int(page))
#         # rooms = paginator.get_page(page),get_page는 try~except 필요없음, paginator.page는 get_page보다 좀 더 에러 컨트롤 할 수 있다.
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")
# ----------------------------------------------------------

# 수동으로 paginator 만들기(1번째 방법,all_rooms func안에 위치)
# page = int(page or 1)  # page= 일 경우 default
# page_size = 10
# limit = page_size * page
# offset = limit - page_size
# all_rooms = models.Room.objects.all()[offset:limit]
# page_count = ceil(models.Room.objects.count() / page_size)
# return render(
#     request,
#     "rooms/home.html",
#     context={
#         "rooms": all_rooms,
#         "page": page,
#         "page_count": page_count,
#         "page_range": range(1, page_count),
#     },
# )
# ======================================================================

# ======================================================================
# CBV(Class Based View)
class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


# ----------------------------------------------------------

# FBV(Function Based View)
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404() #config/settings.py DEBUG=False
#         # return redirect(reverse("core:home"))
# ======================================================================

# ======================================================================
def search(request):
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price  # less than equal

    if guests != 0:
        filter_args["gurests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    rooms = models.Room.objects.filter(**filter_args)

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            rooms = rooms.filter(amenities__pk=int(s_amenity))

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms.filter(facilities__pk=int(s_facility))

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
