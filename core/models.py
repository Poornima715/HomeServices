from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=100)
    email    = models.EmailField(unique=True)
    phone    = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    address  = models.TextField()

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField(unique=True)
    phone        = models.CharField(max_length=15)
    password     = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    location     = models.CharField(max_length=100)
    rating       = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} ({self.service_type})"


class Service(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    provider     = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service      = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status       = models.CharField(max_length=20)

    def __str__(self):
        return f"Booking {self.id} – {self.user.name} with {self.provider.name}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=10, decimal_places=2)
    mode    = models.CharField(max_length=50)
    status  = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment {self.id} – {self.status}"


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating  = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review {self.id} – {self.rating} stars"
