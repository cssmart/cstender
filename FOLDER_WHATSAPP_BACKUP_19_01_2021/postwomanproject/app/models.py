from django.db import models
# Create your models here.

class Mobile_No(models.Model):
    mobile_number = models.CharField(max_length=13, blank=True)
    def __str__(self):
        return self.mobile_number

class CONNECTION_TABLE(models.Model):
    username = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    ip =models.CharField(max_length=20, blank=True)
    port = models.CharField(max_length=4, blank=True)
    service_name = models.CharField(max_length=100, blank=True)
    server = models.CharField(max_length=100, blank=True)
    database_name = models.CharField(max_length=100, blank=True)


class INTERACTION_IN_TABLE(models.Model):
    msg_id = models.CharField(max_length=200, blank=True)
    from_no = models.CharField(max_length=200, blank=True)
    to_no = models.CharField(max_length=200, blank=True)
    timestamp = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=200, blank=True)
    contentType = models.CharField(max_length=200, blank=True)
    attachmentType = models.CharField(max_length=200, blank=True)
    fileLink = models.CharField(max_length=200, blank=True)
    mime_type = models.CharField(max_length=200, blank=True)
    #document
    filename = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    #location
    latitude = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=200, blank=True)




class Whatsapp_Settings(models.Model):
    mobile_no = models.CharField(max_length=10, blank=True)
    key = models.CharField(max_length=200, blank=True)

# class ERP_CONNECTION(models.Model):
#     username = models.CharField(max_length=200, blank=True)
#     password = models.CharField(max_length=200, blank=True)

class General_configuration_chatbot(models.Model):
    time_hour = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    ]
    session_hour = models.CharField(
        max_length=2,
        choices=time_hour
    )
    keyword = models.CharField(max_length=50,blank=True)


class SESSION_WINDOW(models.Model):
    wa_number = models.CharField(max_length=13,blank=True)
    start_timestamp = models.CharField(max_length=100, blank=True)
    updated_timestamp = models.CharField(max_length=100, blank=True)


class WHATSAPP_MAIL(models.Model):
    customer_id=models.CharField(max_length=100, blank=True)
    customer_name = models.CharField(max_length=200,blank=True)
    email_id = models.CharField(max_length=200, blank=True)
    whatsapp_number = models.CharField(max_length=13, blank=True)
    active = models.BooleanField(blank=True, null=True)


    def __str__(self):
        return self.customer_name

class abc(models.Model):
    fileLink = models.FileField(upload_to='Documents_Folder/', blank=True, null=True)



class PALETTE_TABLE(models.Model):
    # palette_category = models.ForeignKey(Content_Type, on_delete=models.CASCADE, null=True)
    # attachment_type = models.ForeignKey(Attachment_Type, on_delete=models.CASCADE, null=True, blank=True)
    p_id = models.CharField(max_length=100, blank=True)
    p_name = models.CharField(max_length=100, blank=True)
    p_type = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(blank=True, null=True)
    p_text = models.TextField(blank=True)
    input_parameter_type = models.CharField(max_length=50, blank=True)
    user_auth_req = models.CharField(max_length=100, blank=True)
    function_id = models.CharField(max_length=100, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    encoded_data = models.TextField(blank=True)
    contentType = models.CharField(max_length=200, blank=True)
    attachmentType = models.CharField(max_length=200, blank=True)
    fileLink = models.CharField(max_length=200, blank=True)
    # fileLink = models.FileField(upload_to='Documents_Folder/', blank=True,null=True)
    mime_type = models.CharField(max_length=200, blank=True)
    # document
    filename = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    # location
    latitude = models.CharField(max_length=200, blank=True)
    label = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=200, blank=True)
    palette_category =models.CharField(choices=[('text', 'Text'),('location', 'Location'), ('media', 'Media')], max_length=100, blank=False)

    def __str__(self):
        return self.p_id
class PALETTE_STRUCTURE(models.Model):
    p_id = models.CharField(max_length=100, blank=True)
    # input_type = models.CharField(max_length=50, blank=True)
    response_text = models.CharField(max_length=200, blank=True)
    callback_p_id = models.CharField(max_length=200, blank=True)
    class Meta:

        ordering = ['-p_id']

    def __str__(self):
        return self.p_id

class INTERACTION_OUT(models.Model):
    session_id= models.CharField(max_length=100, blank=True)
    l_palette_id= models.CharField(max_length=100, blank=True)
    sent_time= models.CharField(max_length=100, blank=True)


class FUNCTION(models.Model):
    f_id = models.CharField(max_length=100, blank=True)
    f_name = models.CharField(max_length=100, blank=True)
    type = [
        ('oracle', 'Oracle'),
        ('sql', 'SQL'),
        ('mysql', 'MYSQL'),
    ]
    connection_type = models.CharField(
        max_length=10,
        choices=type
    )
    executable = models.CharField(max_length=100, blank=True)
