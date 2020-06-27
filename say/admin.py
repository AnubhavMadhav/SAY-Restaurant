from django.contrib import admin
from .models import Contact, Post, BlogComment, Series, Subscriber

# Register your models here.


admin.site.register(Contact)
admin.site.register((BlogComment, Series))
admin.site.register(Subscriber)


# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js',)

    actions = ['send_mail']

    def send_mail(self, request, queryset):
        for post in queryset:
            post.send_mail(request)

    send_mail.short_description = "Send selected Newsletters to all subscribers"


admin.site.register(Post, PostAdmin)