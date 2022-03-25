from django.db import models
from django.db.models import JSONField, F

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from core.validators import JSONSchemaValidator

MY_JSON_FIELD_SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://example.com/object1648177539.json",
    "title": "Root",
    "type": "array",
    "default": [],
    "items": {
        "$id": "#root/items",
        "title": "Items",
        "type": "object",
        "properties": {
            "annotator": {
                "$id": "#root/items/annotator",
                "title": "Annotator",
                "type": "string",
                "default": "",
                "examples": [
                    "vote"
                ],
                "pattern": "^.*$"
            }
        }
    }
}


class Record(models.Model):
    votes = JSONField('votes',
                      default=list,
                      validators=[JSONSchemaValidator(limit_value=MY_JSON_FIELD_SCHEMA)],
                      help_text='Array of annotator votes')
    created_time = models.DateTimeField(auto_now_add=True)


class VoteCounter(models.Model):
    annotator = models.CharField(max_length=100, help_text='Annotator that will make the vote')
    vote = models.CharField(max_length=100, help_text='Vote that the annotator did')
    counter = models.BigIntegerField(default=1)


@receiver(post_save, sender=Record)
def increase_vote_counter(sender, instance, **kwargs):
    vote_items = [next(iter(i.items())) for i in instance.votes]

    for item in vote_items:
        counter, created = VoteCounter.objects.get_or_create(annotator=item[0], vote=item[1])
        if not created:
            counter.counter = F("counter") + 1
            counter.save(update_fields=["counter"])


@receiver(pre_delete, sender=Record)
def decrease_vote_counter(sender, instance, **kwargs):
    vote_items = [next(iter(i.items())) for i in instance.votes]

    for item in vote_items:
        try:
            vote_counter = VoteCounter.objects.get(annotator=item[0], vote=item[1])
            counter = vote_counter.counter - 1
            if counter == 0:
                vote_counter.delete()
            else:
                vote_counter.counter = counter
                vote_counter.save(update_fields=["counter"])
        except VoteCounter.DoesNotExist:
            continue
