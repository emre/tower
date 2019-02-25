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


class AccountFollowerSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['followers']

    def get_followers(self, obj):
        return obj.follower_list


class AccountFollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['following']

    def get_following(self, obj):
        return obj.following_list


class AccountMuterSerializer(serializers.ModelSerializer):
    muters = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['muters']

    def get_muters(self, obj):
        return obj.muter_list


class AccountMutingSerializer(serializers.ModelSerializer):
    muting = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['muting']

    def get_muting(self, obj):
        return obj.muted_list

class ReblogSerializer(serializers.Serializer):
    author = serializers.CharField(source='post__author')
    permlink = serializers.CharField(source='post__permlink')
    created_at = serializers.DateTimeField()
