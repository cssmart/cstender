from django import forms
from .models import CONNECTION_TABLE,General_configuration_chatbot,Whatsapp_Settings,\
    PALETTE_TABLE,PALETTE_STRUCTURE,abc

class ABC(forms.ModelForm):
    class Meta:
        model = abc
        fields = ['fileLink']

class ERP_CONNECTION_FORM(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CONNECTION_TABLE
        fields = ['username', 'password','ip','port','service_name']

    def __init__(self, *args, **kwargs):
        super(ERP_CONNECTION_FORM, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['password'].widget.attrs['style'] = 'width:100%; height:50px;'


class MYSQL_CONNECTION_FORM(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CONNECTION_TABLE
        fields = ['username', 'password','ip','port']

    def __init__(self, *args, **kwargs):
        super(MYSQL_CONNECTION_FORM, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['password'].widget.attrs['style'] = 'width:100%; height:50px;'


class SQL_CONNECTION_FORM(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CONNECTION_TABLE
        fields = ['username', 'password','server','database_name']

    def __init__(self, *args, **kwargs):
        super(SQL_CONNECTION_FORM, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['password'].widget.attrs['style'] = 'width:100%; height:50px;'


class General_configuration_chatbot_form(forms.ModelForm):
    class Meta:
        model = General_configuration_chatbot
        fields = ['session_hour', 'keyword']


class Whatsapp_Settings_Form(forms.ModelForm):
    class Meta:
        model = Whatsapp_Settings
        fields = ['mobile_no', 'key']


class PALETTES_Form(forms.ModelForm):
    class Meta:
        model = PALETTE_TABLE
        fields = ['p_id', 'p_name','p_type','active','input_parameter_type',
                  'user_auth_req','function_id','palette_category']

    def __init__(self, *args, **kwargs):
        super(PALETTES_Form, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        # self.fields['p_text'].widget.attrs['style'] = 'width:100%; height:80px;'
        self.fields['active'].widget.attrs['style'] = 'width:100%; height:50px;'


class Palette_document_send(forms.ModelForm):
    class Meta:
        model = PALETTE_TABLE
        fields = ['fileLink', 'caption','filename','mime_type']

class Palette_video_send(forms.ModelForm):
    class Meta:
        model = PALETTE_TABLE
        fields = ['fileLink','mime_type']

class Palette_image_send(forms.ModelForm):
    class Meta:
        model = PALETTE_TABLE
        fields = ['fileLink','mime_type']


class Palette_location_send(forms.ModelForm):
    class Meta:
        model = PALETTE_TABLE
        fields = ['latitude','longitude']


class Palette_text_send(forms.ModelForm):
    class Meta:
        model = PALETTE_TABLE
        fields = ['p_text']

    def __init__(self, *args, **kwargs):
        super(Palette_text_send, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['p_text'].widget.attrs['style'] = 'width:100%; height:80px;'


class PALETTE_STRUCTURE_Form(forms.ModelForm):
    class Meta:
        model = PALETTE_STRUCTURE
        fields = ['p_id', 'response_text','callback_p_id']