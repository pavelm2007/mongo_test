from datetime import datetime
from mongoengine import *
from mongoengine.django.auth import User
from django.core.urlresolvers import reverse


class Power(Document):
    name = StringField(max_length=200, required=True)
    meta = {'collection': 'Power'}

    def __unicode__(self):
        return self.name


class ImageAlteregos(Document):
    name = StringField(max_length=255, required=False)
    image = ImageField(required=False, thumbnail_size=(100, 100, True))
    # image = ImageField(required=False, thumbnail_size=(100, 100, True))
    meta = {'collection': 'Images'}

class Alteregos(Document):
    # user = ReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField(max_length=200, required=True)
    persone_name = StringField(max_length=200)
    powers = ListField(StringField(max_length=50))
    powers_obj = ReferenceField(Power, reverse_delete_rule=DO_NOTHING, dbref=True)
    powers_obj_list = ListField(ReferenceField(Power, reverse_delete_rule=DO_NOTHING, dbref=True))
    images = ListField(ReferenceField(ImageAlteregos, reverse_delete_rule=DO_NOTHING, dbref=True))
    date_modified = DateTimeField(default=datetime.now())
    is_published = BooleanField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Alteregos, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

    def get_edit_url(self):
        return reverse('update', args=[self.id])

    def get_delete_url(self):
        return reverse('delete', args=[self.id])

    def get_powers_object_id(self):
        if self.powers_obj_list:
            res = []
            for item in self.powers_obj_list:
                res.append(item.id)
            return res
        return None

