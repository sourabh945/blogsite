from rest_framework import serializers 

### import model

from ...models import Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:

        model = Blog

        fields = ['title','id','date_of_pub','author','tags']


        