from bson import ObjectId
from django import forms
from models import *


class AlteregosForm(forms.Form):
    name = forms.CharField(max_length=255)
    persone_name = forms.CharField(max_length=255)
    is_published = forms.BooleanField(required=False)
    powers_obj_list = forms.MultipleChoiceField(required=False)
    powers_obj = forms.ChoiceField(label='Main power')

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(AlteregosForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['persone_name'].initial = self.instance.persone_name
            self.fields['is_published'].initial = self.instance.is_published
            self.fields['powers_obj'].label = 'main power'
            self.fields['powers_obj'].choices = [(obj.id, obj.name) for obj in Power.objects]
            self.fields['powers_obj_list'].choices = [(obj.id, obj.name) for obj in Power.objects]
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        hero = self.instance if self.instance else Alteregos()
        hero.name = self.cleaned_data['name']
        hero.persone_name = self.cleaned_data['persone_name']
        hero.is_published = self.cleaned_data['is_published']
        power_list = self.cleaned_data['powers_obj_list']
        powers = list()
        for power in power_list:
            pow_obj = Power.objects(id=power)[0]
            powers.append(pow_obj)
        hero.powers_obj_list = powers
        powers_obj = Power.objects(id=self.cleaned_data['powers_obj'])[0]

        hero.powers_obj = powers_obj.to_dbref()
        if commit:
            hero.save()

        return hero


class ImageForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(ImageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        image = self.instance if self.instance else ImageAlteregos()
        image.name = self.cleaned_data['name']
        image.image = self.cleaned_data['image']
        if commit:
            image.save()

        return image


class PowerForm(forms.Form):
    name = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(PowerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        power = self.instance if self.instance else Power()
        power.name = self.cleaned_data['name']
        if commit:
            power.save()
        return power


class PowerFilterForm(forms.Form):
    filter = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        # print self.args.get('filter')
        # print kwargs
        super(PowerFilterForm, self).__init__(*args, **kwargs)
        # print Alteregos.objects.filter(is_published=True).only("powers_obj_list")
        choice_power = []
        for hero in Alteregos.objects(is_published=True):
            for obj in hero.powers_obj_list:
                choice_power.append((obj.id, obj.name))
        choice_power = [('all', 'All')] + sorted(set(choice_power))
        self.fields['filter'].choices = choice_power
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

