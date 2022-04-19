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
    room_types = models.RoomType.objects.all()
    return render(
        request,
        "rooms/search.html",
        {"city": city, "countries": countries, "room_types": room_types},
    )
