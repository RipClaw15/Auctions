from django.contrib import admin

from .models import User, Listing, Bid, Comment

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("name",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("auction",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)