from django.db import models
# Create your models here.


class SESSION_WINDOW(models.Model):
    wa_number = models.CharField(max_length=12,blank=True)
    start_timestamp = models.CharField(max_length=100, blank=True)
    updated_timestamp = models.CharField(max_length=100, blank=True)


class PALETTES(models.Model):
    p_id = models.CharField(max_length=100, blank=True)
    p_name = models.CharField(max_length=100, blank=True)
    p_type = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(blank=True)
    p_text = models.CharField(max_length=100, blank=True)
    user_auth_req = models.CharField(max_length=100, blank=True)
    function_id = models.CharField(max_length=100, blank=True)
    input_par_req = models.CharField(max_length=100, blank=True)
    session_id = models.CharField(max_length=100, blank=True)


class PALETTE_STRUCTURE(models.Model):
    p_id = models.CharField(max_length=100, blank=True)
    response_text = models.CharField(max_length=200, blank=True)
    callback_p_id = models.CharField(max_length=200, blank=True)


class INTERACTION_OUT(models.Model):
    session_id= models.CharField(max_length=100, blank=True)
    l_palette_id= models.CharField(max_length=100, blank=True)
    sent_time= models.CharField(max_length=100, blank=True)


class FUNCTION(models.Model):
    F_ID=models.CharField(max_length=100, blank=True)
    F_NAME=models.CharField(max_length=100, blank=True)
    EXECUTABLE=models.CharField(max_length=100, blank=True)
