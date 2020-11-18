# DRF Fancy
I love Django Rest Framework (DRF). It can help us to reduce thousands of lines of code. After a while, I found some 
repeated patterns in my projects, although these patterns are general enough to be a package but not common enough to 
introduced as new features for DRF. So I call them fancy features and decide to write separate code for them instead of 
making pull requests to the original project.   


## Fancy Serializer
If you are going to create a web service with a lot of CRUD resources, ModelSerializer would be very handy. It works 
beautifully, but when it comes to the nested relations, you can't write into them, and you have to overwrite the 
"create" method yourself. FancySerializer is here to fulfill the exact purpose. Here and example:

```python
from django.db import models
from rest_framework import fields, relations

# models
class Role(models.Model):
    name = models.TextField()


class User(models.Model):
    name = models.TextField()
    username = models.TextField(unique=True)
    password = models.TextField()


# serializers
class RoleSerializer(FancySerializer):
    name = fields.CharField()

    class Meta:
        model = Role
        include = ['name']


class UserSerializer(FancySerializer):
    name = fields.CharField(min_length=3, max_length=64)
    username = fields.CharField(min_length=6, max_length=64)
    password = fields.CharField(min_length=8, max_length=64, write_only=True, required=False)
    avatar_pic = fields.CharField(min_length=64, max_length=128, required=False)
    role_id = relations.PrimaryKeyRelatedField(source='role', queryset=Role.objects.all(), required=False)
    role = RoleSerializer(required=False)

    class Meta:
        model = User
        include = ['name',  'username', 'password', 'avatar_pic', 'role_id', 'role']

``` 
