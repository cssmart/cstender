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
    p_text = models.TextField(blank=True)
    input_parameter_type = models.CharField(max_length=50, blank=True)
    user_auth_req = models.CharField(max_length=100, blank=True)
    function_id = models.CharField(max_length=100, blank=True)
    # input_par_req = models.CharField(max_length=100, blank=True)
    session_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.p_name


class PALETTE_STRUCTURE(models.Model):
    p_id = models.CharField(max_length=100, blank=True)
    input_type = models.CharField(max_length=50, blank=True)
    response_text = models.CharField(max_length=200, blank=True)
    callback_p_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.p_id


class INTERACTION_OUT(models.Model):
    session_id= models.CharField(max_length=100, blank=True)
    l_palette_id= models.CharField(max_length=100, blank=True)
    sent_time= models.CharField(max_length=100, blank=True)


class FUNCTION(models.Model):
    f_id = models.CharField(max_length=100, blank=True)
    f_name = models.CharField(max_length=100, blank=True)
    executable = models.CharField(max_length=100, blank=True)
