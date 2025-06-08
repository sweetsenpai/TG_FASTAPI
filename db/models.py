from tortoise import fields, models


class Posts(models.Model):
    """
    Модель поста
    """

    id = fields.IntField(primary_key=True)
    #: Название поста
    title = fields.CharField(max_length=256)
    #: Текст поста
    text = fields.TextField()
    #: Дата создания поста
    date_of_creation = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "posts"


class Users(models.Model):
    """
    Модель пользователя
    """

    id = fields.IntField(primary_key=True)
    #: Email пользователя
    email = fields.CharField(max_length=256, unique=True)
    #: Пароль пользователя
    password = fields.CharField(max_length=256, null=False)
