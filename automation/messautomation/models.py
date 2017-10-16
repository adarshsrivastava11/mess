from __future__ import unicode_literals

from django.db import models

class Extras(models.Model):
	extra_name = models.CharField(max_length=200,blank=True)
	extra_cost = models.IntegerField(default=0,blank=True)
	day_of_week = models.CharField(max_length=500,blank=True)
	
	num = models.IntegerField(default=0,blank=True)
	def __str__(self):
		return self.extra_name

class Student(models.Model):
	name = models.CharField(max_length=200,default="",blank=True)
	roll = models.IntegerField(default=0)
	hall = models.CharField(max_length=10,default="")
	username = models.CharField(max_length=10,default="")
	total_cost = models.IntegerField(default=0)
	recent_item_cost = models.IntegerField(default=0)
	recent_item_name = models.CharField(max_length=200,blank=True)
	all_items_name = models.CharField(max_length=100000,blank=True)
	all_items_quantity = models.CharField(max_length=100000,blank=True)
	all_items_cost = models.CharField(max_length=100000,blank=True)
	all_items_total_cost = models.CharField(max_length=100000,blank=True)
	all_items_date = models.CharField(max_length=100000,blank=True)
	token_ids = models.CharField(max_length=100000,blank=True)
	def __str__(self):
		return str(self.roll)

class Token(models.Model):
	roll = models.CharField(max_length=10,default="")
	name = models.CharField(max_length=10,default="")
	item_taken = models.CharField(max_length=100,default="")
	time_taken = models.CharField(max_length=100,default="")
	total_cost = models.CharField(max_length=100,default="")
	ran_id = models.CharField(max_length=20,default="")
	def __str__(self):
		return self.ran_id
