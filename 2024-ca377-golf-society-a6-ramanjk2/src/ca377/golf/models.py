from django.db import models
from django.urls import reverse

# Create your models here.
class Golfer(models.Model):
	'''Model representing a golfer.'''

	def get_absolute_url(self):
		'''Returns the URL to access a particular instance of Golfer.'''
		return reverse('golferdetails', args=[str(self.id)])

	forename = models.CharField(max_length=50)
	surname = models.CharField(max_length=50)
	handicap = models.IntegerField()

	def __str__(self):
		return '{:s}, {:s}'.format(
			self.surname, self.forename)

	class Meta:
		ordering = ['surname', 'forename']

class GolfCourse(models.Model):
	'''Model representing a golf course.'''

	def get_absolute_url(self):
		'''Returns the URL to access a particular instance of GolfCourse.'''
		return reverse('coursedetails', args=[str(self.id)])

	name = models.CharField(max_length=50)
	latitude = models.DecimalField(null=True, max_digits=5, decimal_places=3)
	longitude = models.DecimalField(null=True, max_digits=6, decimal_places=3)

	def __str__(self):
		return '{:s}'.format(self.name)

	class Meta:
		ordering = ['name']


class WeatherForecast(models.Model):
    date = models.DateField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return f"{self.date} - {self.temperature}°C"
