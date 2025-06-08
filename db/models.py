from tortoise import fields, models


class Posts(models.Model):
    """
    Модель поста
    """

    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=256)
    test = fields.TextField()
    date_of_creation = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "posts"
