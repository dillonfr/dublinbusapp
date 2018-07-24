# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models


# class Leave1(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_1'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave10(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_10'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave11(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_11'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave12(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_12'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave2(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_2'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave3(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_3'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave4(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_4'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave5(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_5'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave6(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_6'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave7(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_7'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave8(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_8'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class Leave9(models.Model):
#     dayofservice = models.DateTimeField(primary_key=True)
#     tripid = models.IntegerField()
#     progrnumber = models.IntegerField()
#     stoppointid = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.TimeField(blank=True, null=True)
#     plannedtime_dep = models.TimeField(blank=True, null=True)
#     actualtime_arr = models.TimeField(blank=True, null=True)
#     actualtime_dep = models.TimeField(blank=True, null=True)
#     vehicleid = models.IntegerField(blank=True, null=True)
#     lastupdate = models.DateTimeField(blank=True, null=True)
#     note = models.CharField(max_length=400, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'Leave_9'
#         unique_together = (('dayofservice', 'tripid', 'progrnumber'),)


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=80)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


# class DublinbusappBus(models.Model):
#     bus_id = models.CharField(max_length=10)
#     route = models.CharField(max_length=10)
#     journey_time = models.CharField(max_length=100)
#     bus_logo = models.CharField(max_length=1000)

#     class Meta:
#         managed = False
#         db_table = 'dublinbusapp_bus'


# class DublinbusappPassenger(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.CharField(max_length=5)
#     bus = models.ForeignKey(DublinbusappBus, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'dublinbusapp_passenger'


# class Sample(models.Model):
#     id = models.IntegerField(primary_key=True)

#     class Meta:
#         managed = False
#         db_table = 'sample'


# class Trips2016(models.Model):
#     data_source = models.CharField(max_length=10, blank=True, null=True)
#     day_of_service = models.CharField(max_length=50)
#     tripid = models.CharField(primary_key=True, max_length=30)
#     lineid = models.CharField(max_length=30, blank=True, null=True)
#     routeid = models.CharField(max_length=30, blank=True, null=True)
#     direction = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.IntegerField(blank=True, null=True)
#     plannedtime_dep = models.IntegerField(blank=True, null=True)
#     actualtime_arr = models.IntegerField(blank=True, null=True)
#     actualtime_dep = models.IntegerField(blank=True, null=True)
#     basin = models.CharField(max_length=30, blank=True, null=True)
#     tenderlot = models.CharField(max_length=30, blank=True, null=True)
#     suppressed = models.CharField(max_length=30, blank=True, null=True)
#     justification = models.CharField(max_length=30, blank=True, null=True)
#     lastupdate = models.CharField(max_length=50, blank=True, null=True)
#     note = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'trips2016'
#         unique_together = (('tripid', 'day_of_service'),)


# class Trips2017(models.Model):
#     data_source = models.CharField(max_length=10, blank=True, null=True)
#     day_of_service = models.CharField(max_length=50, blank=True, null=True)
#     tripid = models.CharField(max_length=30, primary_key=True)
#     lineid = models.CharField(max_length=30, blank=True, null=True)
#     routeid = models.CharField(max_length=30, blank=True, null=True)
#     direction = models.IntegerField(blank=True, null=True)
#     plannedtime_arr = models.IntegerField(blank=True, null=True)
#     plannedtime_dep = models.IntegerField(blank=True, null=True)
#     actualtime_arr = models.IntegerField(blank=True, null=True)
#     actualtime_dep = models.IntegerField(blank=True, null=True)
#     basin = models.CharField(max_length=30, blank=True, null=True)
#     tenderlot = models.CharField(max_length=30, blank=True, null=True)
#     suppressed = models.CharField(max_length=30, blank=True, null=True)
#     justification = models.CharField(max_length=30, blank=True, null=True)
#     lastupdate = models.CharField(max_length=50, blank=True, null=True)
#     note = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'trips2017'
