from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    ignored = models.BooleanField(default=False)

    def ignore(self):
        Position.objects.filter(company=self).delete()
        self.ignored = True
        self.save()

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ' :: ' + self.company.name
