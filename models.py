from tortoise import fields, models


class Users(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    #: This is a username
    username = fields.CharField(max_length=20, unique=True)
    role = fields.CharField(max_length=30, default="user")
    #: This will hold the auth key to the API
    password_hash = fields.CharField(max_length=128, null=True)
    age = fields.IntField()
    phone_number = fields.CharField(max_length=20, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class PydanticMeta:
        # computed = ["full_name"]
        exclude = ["password_hash", "results"]


class TestResults(models.Model):
    """
    Test Results
    """
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField(
        "models.Users",
        related_name="user_results",
        description="FK to Users"
    )


class TestSession(models.Model):
    """
    Test Session
    """
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True)
    test_result: fields.ForeignKeyRelation[TestResults] = fields.ForeignKeyField(
        "models.TestResults",
        related_name="test_session",
        description="FK to test_session"
    )


class FatigueTest(models.Model):
    """
    Fatigue Test
    """
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True)
    test_session: fields.ForeignKeyRelation[TestSession] = fields.ForeignKeyField(
        "models.TestSession",
        related_name="fatigue_test",
        description="FK to fatigue_test"
    )
    blink_time = fields.DatetimeField(auto_now=False)
    blink_duration = fields.FloatField()


class SustainedAttentionTest(models.Model):
    """
    Sustained Attention Test
    """
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True)
    test_session: fields.ForeignKeyRelation[TestSession] = fields.ForeignKeyField(
        "models.TestSession",
        related_name="attention_test",
        description="FK to attention_test"
    )
    number_shown_time = fields.DatetimeField()
    button_pressed_time = fields.DatetimeField()
    number_shown = fields.IntField()
    button_pressed = fields.BooleanField()
