from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify


class Client(models.Model):
    client_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], unique=True
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(blank=True)
    registration_date = models.DateField()
    address = models.CharField(max_length=50, blank=True)
    email_address = models.EmailField("Client email")
    slug = models.SlugField()

    def __str__(self):
        return str(self.client_number) + " " + self.first_name + " " + self.last_name

    def slug(self):
        return slugify(self.client_number)


# c = Client(client_number = 548, first_name = "Ivan", last_name = "Rivero", birthdate = "05.08.1986", registration_date = "23.03.2021", email_address = "test@gmail.com")


class Series(models.Model):
    publisher = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    volume = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    slug = models.SlugField()

    def __str__(self):
        return self.name + " Volume " + str(self.volume)

    def slug(self):
        return slugify(self.id)


# s = Series(publisher = "DC", name = "Batman", volume = 3)


class Comic(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    issue = models.IntegerField()
    pub_date = models.DateField()
    price = models.FloatField()
    writer = models.CharField(max_length=60, blank=True)
    penciller = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return str(self.series) + " " + str(self.issue)


# co = Comic(series = Series.objects.get(publisher = "Marvel", name = "X-Men", volume = 1), issue = 1, pub_date = "2021-03-03")


class Subscription(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.client) + " " + str(self.series)


# su = Subscription(series = Series.objects.get(publisher = "Marvel", name = "X-Men", volume = 1),
