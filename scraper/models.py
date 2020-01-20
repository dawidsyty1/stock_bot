from django.db import models

from django.db import models

TYPE = (
    ('image', 'image'),
    ('text', 'text'),
)


class Task(models.Model):
    STATUS = (
        ('new', 'new'),
        ('inprogress', 'inprogress'),
        ('succeed', 'succeed'),
        ('abandoned', 'abandoned'),
    )
    url = models.URLField(max_length=300, default='')
    status = models.CharField(max_length=10, default='new', choices=STATUS)
    counter = models.IntegerField(default=0)
    type = models.CharField(max_length=10, default='text', choices=TYPE)

    def set_as_new(self):
        self.status = 'new'
        self.counter = 0
        self.save()

    def is_to_abandon(self):
        if self.counter > 2:
            return False
        return True

    def set_as_abandoned(self):
        self.status = 'abandoned'
        self.save()

    def set_as_inprogress(self):
        self.counter = self.counter + 1
        self.status = 'inprogress'
        self.save()

    def set_as_succeed(self):
        self.status = 'succeed'
        self.save()


class Resource(models.Model):
    site_name = models.URLField(max_length=300, default='')
    file_name = models.CharField(max_length=200, default='not_available')
    path = models.CharField(max_length=200, default='not_available')
    type = models.CharField(max_length=10, default='text', choices=TYPE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True)
    status = models.CharField(max_length=200, default='')

    def build_download_url(self, absolute_url):
        if self.file_name == 'not_available':
            return "Not available downloads url"
        return absolute_url + "/{}/".format(self.id)

    def set_status(self, status):
        self.status = (status[:200] + '..') if len(status) > 200 else status
