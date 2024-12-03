from rest_framework import serializers

from ...models import Blog

class Blog_foramtter(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title' , 'date_of_pub' , 'content' , 'tags' , 'author' ]