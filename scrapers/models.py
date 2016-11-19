from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    ignored = models.BooleanField(default=False)

    def ignore(self):
        self.ignored = true
        Position.objects.filter(company=self).delete()

class Position(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
