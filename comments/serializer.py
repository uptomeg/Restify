from rest_framework.serializers import ModelSerializer
import sys
# sys.path.insert(1, '/group_2256/P2/restify/p2/comments')
from comments.models import UserComment, PropertyComment


class UserCommentSerializer(ModelSerializer):
    class Meta:
        model = UserComment
        fields = '__all__'
        read_only_fields = ('owner', 'under', 'parent', 'date')


class PropertyCommentSerializer(ModelSerializer):
    class Meta:
        model = PropertyComment
        fields = '__all__'
        read_only_fields = ('owner', 'under', 'parent', 'date')
