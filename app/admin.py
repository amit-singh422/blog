from django.contrib import admin
from app.models import Post

# Register your models here.

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display=['id','title','desc']