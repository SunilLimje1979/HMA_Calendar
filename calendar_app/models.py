from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TopBanner(models.Model):
    topbanner_id = models.AutoField(primary_key=True)
    topbanner_image = models.TextField() #to add path to image
    topbanner_large_image = models.TextField(null=True,blank=True) # to add path  to image
    topbanner_website = models.TextField(null=True,blank=True) #to add website link
    topbanner_order = models.IntegerField(null=True,blank=True)
    topbanner_status = models.IntegerField(default=1,null=True,blank=True) #1=Active,0=deactive
    topbanner_month = models.IntegerField(null=True,blank=True)
    topbanner_year = models.CharField(null=True,blank=True)
    #############Bydefault fields####################
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_reason = models.CharField(max_length=100, blank=True, null=True)
   
    class Meta:
       db_table = 'TopBanner'

class BottomBanner(models.Model):
    bottombanner_id = models.AutoField(primary_key=True)
    bottombanner_image = models.TextField() #to add path to image
    bottombanner_large_image = models.TextField(null=True,blank=True) # to add path  to image
    bottombanner_website = models.TextField(null=True,blank=True) #to add website link
    bottombanner_order = models.IntegerField(null=True,blank=True)
    bottombanner_status = models.IntegerField(default=1,null=True,blank=True) #1=Active,0=deactive
    bottombanner_month = models.IntegerField(null=True,blank=True)
    bottombanner_year = models.CharField(null=True,blank=True)
    #############Bydefault fields####################
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_reason = models.CharField(max_length=100, blank=True, null=True)
   
    class Meta:
       db_table = 'BottomBanner'

class MiddleBanner(models.Model):
    middlebanner_id = models.AutoField(primary_key=True)
    middlebanner_image = models.TextField()
    middlebanner_month = models.IntegerField(null=True,blank=True)
    middlebanner_year = models.CharField(null=True,blank=True)

    #############Bydefault fields####################
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_reason = models.CharField(max_length=100, blank=True, null=True)
   
    class Meta:
       db_table = 'MiddleBanner'


class EventManagement(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=500,null=True,blank=True)
    event_details = models.TextField(null=True,blank=True)
    event_status = models.IntegerField(default=1,null=True,blank=True) # 1=Active 0=Deactive
    event_datetime = models.DateTimeField(null=True,blank=True)
    event_month = models.IntegerField(null=True,blank=True)
    event_year = models.CharField(max_length=255,null=True,blank=True)
    event_date = models.IntegerField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    #############Bydefault fields####################
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_reason = models.CharField(max_length=100, blank=True, null=True)
   
    class Meta:
       db_table = 'EventManagement'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True) # Unique ensures no duplicates

    class Meta:
       db_table = 'UserProfile'

    def __str__(self):
        return self.user.username