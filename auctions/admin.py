from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ["watchlist"]


class AuctionListingInline(admin.StackedInline):
    model = AuctionListing


class AuctionCategoryAdmin(admin.ModelAdmin):
    inlines = [AuctionListingInline]


class BidInline(admin.TabularInline):
    model = Bid


class CommentInline(admin.TabularInline):
    model = Comment


class AuctionListingAdmin(admin.ModelAdmin):
    inlines = [BidInline, CommentInline]


# Register your models here.
admin.site.register(AuctionCategory, AuctionCategoryAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
