from django.db import models
from django.contrib.postgres.fields import ArrayField

""" Modules models for Mobile App
"""


class Modules(models.Model):
    slug = models.CharField(max_length=100, blank=False)
    title = models.CharField(max_length=500, blank=False)
    icon = models.CharField(max_length=100, blank=False)
    version = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000, blank=False)

    class Meta:
        unique_together = ('slug', 'version',)

    def save(self, *args, **kwargs):
        module = Modules.objects.filter(slug=self.slug, version=self.version).first()
        if module is not None:
            raise Exception('Unique Constraint violation: (app_version, slug) pair must be unique')
        super().save(*args, **kwargs)

    def partial_update(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        super().save()


class ModulesByApp(models.Model):
    appVersion = models.CharField(max_length=100, blank=False)
    moduleSlug = models.CharField(max_length=500, blank=False)
    moduleVersion = models.CharField(max_length=100, blank=False)
    status = models.IntegerField(default=1, blank=False)

    def save(self, *args, **kwargs):
        module_by_app = ModulesByApp.objects.filter(appVersion=self.appVersion, moduleSlug=self.moduleSlug).first()
        if module_by_app is not None:
            raise Exception('Unique Constraint violation: (app_version, slug) pair must be unique')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        modules_by_app = list(ModulesByApp.objects.filter(appVersion=self.appVersion, moduleSlug=self.moduleSlug).all())
        if len(modules_by_app) == 1:
            module_order = ModuleOrder.objects.filter(appVersion=self.appVersion).first()
            if module_order is not None:
                module_order.order = [x for x in module_order.order if x != self.moduleSlug]
                module_order.save()
        super().delete(*args, **kwargs)

    def partial_update(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        super().save()


class ModuleOrder(models.Model):
    appVersion = models.CharField(max_length=100, blank=False, unique=True, primary_key=True)
    order = ArrayField(models.CharField(max_length=500, blank=False), blank=False)
