from django.contrib import admin
from django.utils.html import mark_safe
from . import models


# Register your models here.
@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)

    # Rooms 정보 카테고리로 구성 셋
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 접을 수 있는 섹션으로 만들 수 있다.
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    # 원하는 항목만 리스트로 화면 출력
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    # 정렬
    ordering = ("name", "price", "bedrooms")

    # 오른쪽 카테고리 필터
    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # user가 많을수록 list형 선택은 불편해져서 id형으로 관리
    raw_id_fields = ("host",)

    # 검색 설정
    search_fields = ("city", "^host__username")

    # many_to_many 항목 편집을 편하게
    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):  # self: admin class(RoomAdmin), obj: 현재 row
        # print(obj.amenities.all())  # console에 현재 row 출력
        return obj.amenities.count()

    # count_amenities.short_description = "hello sexy!" 표시될 이름 바꾸기

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"
