from django.db import models
from django.contrib.auth.models import User, Group


class Customer(models.Model):
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	email = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	mobile = models.CharField(max_length=20)
	company_name = models.CharField(max_length=250)
	sales_contact = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="customers"
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.company_name})"

class ContractStatus(models.Model):
	label = models.CharField(max_length=100)

	def __str__(self):
		return f"contract status: {self.label}"

class Contract(models.Model):
	customer = models.ForeignKey(
		to=Customer,
		on_delete=models.CASCADE,
		related_name="contracts"
	)
	sales_contact = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="contracts"
	)
	status = models.ForeignKey(
		to=ContractStatus,
		on_delete=models.CASCADE
	)
	amount = models.FloatField()
	payment_due = models.DateTimeField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"contract for {self.customer}"

class EventStatus(models.Model):
	label = models.CharField(max_length=100)

	def __str__(self):
		return f"event status: {self.label}"

class Event(models.Model):
	customer = models.ForeignKey(
		to=Customer,
		on_delete=models.CASCADE,
		related_name="events"
	)
	# contract = models.ForeignKey(
	# 	to=Contract,
	# 	on_delete=models.CASCADE,
	# 	related_name="events"
	# )
	support_contact = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="events"
	)
	status = models.ForeignKey(
		to=EventStatus,
		on_delete=models.CASCADE
	)
	date = models.DateTimeField()
	number_of_attendees = models.IntegerField()
	notes = models.TextField(max_length=2048, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"event for {self.customer}"
