from peewee import Model, SqliteDatabase, AutoField, CharField, TextField, FloatField, DateTimeField,IntegerField
from datetime import datetime, timezone

db = SqliteDatabase("tickets.db")

class Ticket(Model):
    id = AutoField()
    user_id = CharField()
    order_id = CharField()
    problem_text = TextField()
    image_url = CharField(null=True)
    caption = TextField(null=True)
    final_confidence = FloatField(null=True)
    decision = CharField(null=True)
    status = CharField(default="Pending")
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    restaurant_name=CharField()
    reply_tag=CharField(null=True)
    reply_text=TextField(null=True)
    

    class Meta:
        database = db
class Restaurant(Model):
    id = AutoField()
    name = CharField(unique=True)
    problem_count = IntegerField(default=0)
    rating = CharField(default="Normal")

    class Meta:
        database = db

# Init DB
db.connect()
db.create_tables([Ticket, Restaurant])
