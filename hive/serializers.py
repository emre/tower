from rest_framework import serializers

from .models import Account, Block, Post, PostCache, State


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('__all__')


class LightPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'is_deleted', 'is_pinned',
            'is_muted', 'is_valid', 'promoted', 'parent', 'community'
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')


class PostCacheSerializer(serializers.ModelSerializer):
    post = LightPostSerializer()

    class Meta:
        model = PostCache
        fields = ('__all__')


class HiveStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('__all__')