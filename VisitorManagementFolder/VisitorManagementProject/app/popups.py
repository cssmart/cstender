from string import ascii_uppercase
from django.views.generic import TemplateView
import cx_Oracle
from django_popup_view_field.registry import registry_popup_view

class MeetPersonPopupView(TemplateView):
    template_name = "popups/popup_meet_person_list.html"
    item = None

    def get(self, request, *args, **kwargs):
        code_val = []
        desc_val =[]
        pum= []
        if "name" in request.GET:
            name = request.GET.get('name')
            listdata = ['harshita','test','ABC','aharshita31@gmail.com']
            if name in str(listdata):
                code_val.append(name)
        list_val = code_val
        qs = list_val
        self.item = qs
        return super(MeetPersonPopupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MeetPersonPopupView, self).get_context_data(**kwargs)

        context['item'] = self.item
        context['ascii_uppercase'] = ascii_uppercase
        return context

registry_popup_view.register(MeetPersonPopupView)
