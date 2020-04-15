from string import ascii_uppercase
from django.views.generic import TemplateView
from django_popup_view_field.registry import registry_popup_view


class MeetPersonPopupView(TemplateView):
    template_name = "popups/popup_meet_person_list.html"
    item = None

    def get(self, request, *args, **kwargs):
        code_val = []
        desc_val =[]
        pum= []
        if "code" in request.GET or "name" in request.GET:
            name = request.GET.get('name')
            code = request.GET.get('code')
            listdata = ['Harshita','test','ABC','aharshita31@gmail.com']
            if code:
                res = [idx for idx in listdata if idx.lower().startswith(code.lower())]
                for i in res:
                    code_val.append(i)
            elif name in str(listdata):
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


class HostNAmePopupView(TemplateView):
    template_name = "popups/popup_host_name_list.html"
    item = None

    def get(self, request, *args, **kwargs):
        code_val = []
        if "code" in request.GET or "name" in request.GET:
            name = request.GET.get('name')
            code = request.GET.get('name')
            listdata = ['harshita','test','ABC','aharshita31@gmail.com']
            if name in str(listdata) or code in str(listdata):
                code_val.append(name)
                code_val.append(code)
        list_val = code_val
        qs = list_val
        self.item = qs
        return super(HostNAmePopupView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HostNAmePopupView, self).get_context_data(**kwargs)

        context['item'] = self.item
        context['ascii_uppercase'] = ascii_uppercase
        return context

# class HostNAmePopupView(TemplateView):
#
#     template_name = "popups/popup_host_name_list.html"
#     countries = None
#
#     def get(self, request, *args, **kwargs):
#         qs =  ['harshita','test','ABC','aharshita31@gmail.com']
#         if "code" in request.GET or "name" in request.GET:
#             qs =  ['harshita','test','ABC','aharshita31@gmail.com']
#             if "code" in request.GET:
#                 qs = qs.filter(code__istartswith=request.GET.get('code'))
#             if "name" in request.GET:
#                 qs = qs.filter(name__icontains=request.GET.get('name'))
#
#         self.countries = qs
#         return super(HostNAmePopupView, self).get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(HostNAmePopupView, self).get_context_data(**kwargs)
#         context['countries'] = self.countries
#         context['ascii_uppercase'] = ascii_uppercase
#         return context



registry_popup_view.register(MeetPersonPopupView)
registry_popup_view.register(HostNAmePopupView)
