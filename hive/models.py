from django.db import models


class Account(models.Model):
    name = models.CharField(unique=True, max_length=16)
    created_at = models.DateTimeField()
    reputation = models.FloatField()
    display_name = models.CharField(max_length=20, blank=True, null=True)
    about = models.CharField(max_length=160, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.CharField(max_length=1024)
    cover_image = models.CharField(max_length=1024)
    followers = models.IntegerField()
    following = models.IntegerField()
    proxy = models.CharField(max_length=16)
    post_count = models.IntegerField()
    proxy_weight = models.FloatField()
    vote_weight = models.FloatField()
    kb_used = models.IntegerField()
    rank = models.IntegerField()
    active_at = models.DateTimeField()
    cached_at = models.DateTimeField()
    raw_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hive_accounts'
        ordering = ['-pk']


class Block(models.Model):
    num = models.IntegerField(primary_key=True)
    hash = models.CharField(unique=True, max_length=40)
    prev = models.ForeignKey('self', models.DO_NOTHING, db_column='prev',
                             blank=True, null=True)
    txs = models.SmallIntegerField()
    ops = models.SmallIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hive_blocks'
        ordering = ['-num']



class Community(models.Model):
    name = models.ForeignKey(Account, models.DO_NOTHING, db_column='name',
                             primary_key=True)
    title = models.CharField(max_length=32)
    about = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    lang = models.CharField(max_length=2)
    settings = models.TextField()
    type_id = models.SmallIntegerField()
    is_nsfw = models.BooleanField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hive_communities'


class FeedCache(models.Model):
    post_id = models.IntegerField()
    account_id = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hive_feed_cache'
        unique_together = (('post_id', 'account_id'),)


class Flag(models.Model):
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='account')
    post = models.ForeignKey('Post', models.DO_NOTHING)
    created_at = models.DateTimeField()
    notes = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'hive_flags'
        unique_together = (('account', 'post'),)


class Follow(models.Model):
    follower = models.IntegerField()
    following = models.IntegerField()
    state = models.SmallIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hive_follows'
        unique_together = (('following', 'follower'),)


class Member(models.Model):
    community = models.ForeignKey(Community, models.DO_NOTHING,
                                  db_column='community')
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='account')
    is_admin = models.BooleanField()
    is_mod = models.BooleanField()
    is_approved = models.BooleanField()
    is_muted = models.BooleanField()
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'hive_members'
        unique_together = (('community', 'account'),)


class Modlog(models.Model):
    community = models.ForeignKey(Community, models.DO_NOTHING,
                                  db_column='community')
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='account')
    action = models.CharField(max_length=32)
    params = models.CharField(max_length=1000)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hive_modlog'


class Payment(models.Model):
    block_num = models.IntegerField()
    tx_idx = models.SmallIntegerField()
    post = models.ForeignKey('Post', models.DO_NOTHING)
    from_account = models.ForeignKey(Account, models.DO_NOTHING,
                                     db_column='from_account', related_name="from_acc")
    to_account = models.ForeignKey(Account, models.DO_NOTHING,
                                   db_column='to_account', related_name="to_acc")
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    token = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'hive_payments'


class PostTag(models.Model):
    post_id = models.IntegerField()
    tag = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'hive_post_tags'
        unique_together = (('tag', 'post_id'),)


class Post(models.Model):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    author = models.ForeignKey(Account, models.DO_NOTHING, db_column='author', related_name="author")
    permlink = models.CharField(max_length=255)
    community = models.ForeignKey(Account, models.DO_NOTHING,
                                  db_column='community')
    category = models.CharField(max_length=255)
    depth = models.SmallIntegerField()
    created_at = models.DateTimeField()
    is_deleted = models.BooleanField()
    is_pinned = models.BooleanField()
    is_muted = models.BooleanField()
    is_valid = models.BooleanField()
    promoted = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'hive_posts'
        unique_together = (('author', 'permlink'),)


class PostCache(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=16)
    permlink = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    depth = models.SmallIntegerField()
    children = models.SmallIntegerField()
    author_rep = models.FloatField()
    flag_weight = models.FloatField()
    total_votes = models.IntegerField()
    up_votes = models.IntegerField()
    title = models.CharField(max_length=255)
    preview = models.CharField(max_length=1024)
    img_url = models.CharField(max_length=1024)
    payout = models.DecimalField(max_digits=10, decimal_places=3)
    promoted = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField()
    payout_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_paidout = models.BooleanField()
    is_nsfw = models.BooleanField()
    is_declined = models.BooleanField()
    is_full_power = models.BooleanField()
    is_hidden = models.BooleanField()
    is_grayed = models.BooleanField()
    rshares = models.BigIntegerField()
    sc_trend = models.FloatField()
    sc_hot = models.FloatField()
    body = models.TextField(blank=True, null=True)
    votes = models.TextField(blank=True, null=True)
    json = models.TextField(blank=True, null=True)
    raw_json = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hive_posts_cache'


class Reblog(models.Model):
    account = models.ForeignKey(Account, models.DO_NOTHING, db_column='account')
    post = models.ForeignKey(Post, models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hive_reblogs'
        unique_together = (('account', 'post'),)


class State(models.Model):
    block_num = models.IntegerField(primary_key=True)
    db_version = models.IntegerField()
    steem_per_mvest = models.DecimalField(max_digits=8, decimal_places=3)
    usd_per_steem = models.DecimalField(max_digits=8, decimal_places=3)
    sbd_per_steem = models.DecimalField(max_digits=8, decimal_places=3)
    dgpo = models.TextField()

    class Meta:
        managed = False
        db_table = 'hive_state'
