from django.shortcuts import render
from django.shortcuts import render, redirect
from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url
from . import forms, models
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from formtools.wizard.views import SessionWizardView
from django.template import RequestContext
from django.db import connection, transaction
from django.http import JsonResponse, QueryDict
from django.db import connection


class FirstTenderView(StartFlowMixin, SessionWizardView):
    template_name = 'app/app/first_sample.html'
    form_list = [forms.TenderDetailForm, forms.BodyDetailsForm]

    def done(self, form_list, form_dict, **kwargs):
        tender = form_dict['0'].save()
        self.request.session['tend_id'] = tender.id
        body = form_dict['1'].save(commit=False)
        body.tender_id = tender
        body.save()
        self.activation.process.body = body
        self.activation.done()
        return redirect(get_next_task_url(self.request, self.activation.process))


from django.db import connection
@flow_view
def add_board_summary(request, **kwargs):
    tender_id_data = request.session.get('tend_id')
    print(tender_id_data,'qqqqqqqqqqqqqqwwwwwwwwwwwwwwwwwwwwwww')
    request.session['id_tender'] = tender_id_data
    print(request.session['id_tender'], 'sssssssssssssssssssssssssssssssssssssssssss')
    request.activation.prepare(request.POST or None)
    form = forms.BoardDetailForm(request.POST or None)
    board_form = forms.BoardForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            board_code = form.cleaned_data['board_code']
            board_desc = form.cleaned_data['board_desc']
            stand_or_non = form.cleaned_data['stand_or_non']
            indoor_or_outdoor = form.cleaned_data['indoor_or_outdoor']
            mcc_or_nonstan = form.cleaned_data['mcc_or_nonstan']
            board_qty = form.cleaned_data['board_qty']
            mcc_description = form.cleaned_data['mcc_description']
            hori_bus_bar_desc = form.cleaned_data['hori_bus_bar_desc']
            control_bus_bar_qty = form.cleaned_data['control_bus_bar_qty']
            front_access_panel = form.cleaned_data['front_access_panel']
            phase = form.cleaned_data['phase']
            board_save = models.BoardDetails(board_code=board_code, board_desc=board_desc, tender_id=tender_id_data,
                                             stand_or_non=stand_or_non, indoor_or_outdoor=indoor_or_outdoor,
                                             mcc_or_nonstan=mcc_or_nonstan, board_qty=board_qty, mcc_description=mcc_description,
                                             hori_bus_bar_desc=hori_bus_bar_desc, front_access_panel=front_access_panel,
                                             phase=phase, control_bus_bar_qty=control_bus_bar_qty)
            board_save.save()
            return redirect('.')
    if request.method == 'POST':
        if board_form.is_valid():
            board_code = request.POST.get('board_code')
            print(board_code,'ddddddddddddddddd')
            queryset = models.BOARDS.objects.filter(BRD_CODE=board_code).distinct('BRD_CODE')
            if queryset:
                for i in queryset:
                    p = models.BoardDetails(board_code=board_code, board_desc=i.BRD_DESC, tender_id=tender_id_data)
                    p.save()
            return redirect('.')
        else:
            print(form.errors)
    # elif request.POST:
    #     return redirect(get_next_task_url(request, request.activation.process))
    board_form = forms.BoardForm()
    form = forms.BoardDetailForm()
    model_data = models.BoardDetails.objects.filter(tender_id=tender_id_data)
    return render(request, 'app/app/list_board.html', {
        'form': form,
        'board_form':board_form,
        'model_data': model_data,
        'activation': request.activation
    })


# from django.db import connection
# @flow_view
# def add_board_summary(request, **kwargs):
#     action_list = []
#     tender_id_data = request.session.get('tend_id')
#     request.activation.prepare(request.POST or None)
#     form = forms.BoardDetailForm(request.POST or None)
#     print(form.is_valid(),'21wssssss')
#     if form.is_valid():
#         form.save(commit=False)
#         board_code = form.cleaned_data['board_code']
#         queryset = models.BoardsTableData.objects.filter(brd_code=board_code)
#         print(queryset,'qqqqqqqqqqqqqqq')
#         if queryset:
#             for i in queryset:
#                 a = models.BoardDetails.objects.filter(board_code=i).update(board_desc=i.brd_desc)
#                 print(a,'wwwwwwwwwwwwwwwwwwwwwwww')
#                 brd_desc = request.GET.get(i.brd_desc)
#                 print(brd_desc,'2fffffffffffffffffffffff')
#                 # data = request.GET.get(i.brd_desc)
#                 data = i.brd_desc
#                 # data = models.BoardDetails.objects.create(board_desc=i.brd_desc)
#                 print(data,'11111111111111118888888888888')
#                 # a = queryset.update(brd_desc=data)
#                 # print(a, '===========================')
#                 # cursor = connection.cursor()
#                 # cursor.execute("SELECT  brd_desc FROM  app_boardstabledata WHERE  brd_code ='B0001'")
#                 # result = cursor.fetchall()
#                 # print(result, '12222222222223333333333333333333333333333333')
#                 board_c = i
#                 print(board_c, '2222222222222222222222222222222222')
#                 #                 # board_desc = result[0]
#                 # print(board_desc, 'board desc================================')
#         # s = models.BoardDetails(board_code=board_c, board_desc=data)
#         # s.save()
#         # print(s,'qqqqqqqqqqqqqqqqqqqqq')
#         stand_or_non = form.cleaned_data['stand_or_non']
#         indoor_or_outdoor = form.cleaned_data['indoor_or_outdoor']
#         mcc_or_nonstan = form.cleaned_data['mcc_or_nonstan']
#         board_qty = form.cleaned_data['board_qty']
#         mcc_description = form.cleaned_data['mcc_description']
#         hori_bus_bar_desc = form.cleaned_data['hori_bus_bar_desc']
#         control_bus_bar_qty = form.cleaned_data['control_bus_bar_qty']
#         front_access_panel = form.cleaned_data['front_access_panel']
#         phase = form.cleaned_data['phase']
#         p = models.BoardDetails(tender_id=tender_id_data,
#                                 stand_or_non=stand_or_non, indoor_or_outdoor=indoor_or_outdoor,
#                                 mcc_or_nonstan=mcc_or_nonstan, board_qty=board_qty, mcc_description=mcc_description,
#                                 hori_bus_bar_desc=hori_bus_bar_desc, front_access_panel=front_access_panel,
#                                 phase=phase, control_bus_bar_qty=control_bus_bar_qty)
#         p.save()
#         return redirect('.')
#     elif request.POST:
#         return redirect(get_next_task_url(request, request.activation.process))
#     form = forms.BoardDetailForm()
#     model_data = models.BoardDetails.objects.filter(tender_id=tender_id_data)
#     return render(request, 'app/app/list_board.html', {
#         'form': form,
#         'model_data': model_data,
#         'activation': request.activation
#     })

def add_board_detail(request, **kwargs):
    new_item = get_object_or_404(models.BoardDetails,  pk=kwargs['pk'])
    queryset = models.BoardDetails.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(board_code=i.board_code, board_desc=i.board_desc,mcc_description=i.mcc_description,
                               stand_or_non=i.stand_or_non, indoor_or_outdoor=i.indoor_or_outdoor,
                               mcc_or_nonstan=i.mcc_or_nonstan, board_qty=i.board_qty,
                               hori_bus_bar_desc=i.hori_bus_bar_desc, front_access_panel=i.front_access_panel,
                               phase=i.phase, control_bus_bar_qty=i.control_bus_bar_qty)
    form = forms.BoardDetailForm(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('.')
    context = {
        "form": form,
    }
    return render(request, "app/app/board_form.html", context)
#
# from django.contrib import messages
# @flow_start_view
# def add_module_list(request, **kwargs):
#     tender_id_data = request.session.get('tend_id')
#     article = get_object_or_404(models.BoardDetails,  pk=kwargs['pk'])
#     form = forms.BoardDetailForm(request.POST or None, instance=article)
#     edit_form = forms.ModuleDetailForm(request.POST or None)
#     if form.is_valid():
#         article = form.save()
#     if edit_form.is_valid():
#         edit = edit_form.save(commit=False)
#         edit.board_detail = article
#         edit.save()
#         msg = "Article updated successfully"
#         messages.success(request, msg, fail_silently=True)
#         return redirect(article)
#     return render(request, 'app/app/add_module.html', {
#             'form': form,
#             'activation': request.activation
#         })
#     return render(request, 'app/app/add_module.html', {'form': form, 'edit_form': edit_form, 'article':article })

    #  queryset = models.BoardDetails.objects.filter(pk=kwargs['pk'])
    # print(queryset,'querysettttttttttttttttttttttt')
    # data =models.ModuleDetails
    # print(data.board_detail,'ooooooooooooooooooooooooooooooooooooooo')
    # data.board_detail = new_item
    # print(data.board_detail,'lllllllllllllllllllllllllllllllllllll')

#
# def add_module_list(request, **kwargs):
#     tender_i = request.session.get('id_tender')
#     new_item = get_object_or_404(models.BoardDetails, pk=kwargs['pk'])
#     print(new_item, "new item")
#     form = forms.ModuleDetailForm(request.POST, instance=new_item)
#     print(form.is_valid(),'lllllllllllllllllllllllllllllllllllllllll')
#     if form.is_valid():
#         form.tender_id =tender_i
#         print(form.tender_id,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
#         form.save()
#         return redirect('.')
#     form = forms.ModuleDetailForm()
#     return render(request, 'app/app/addmodule.html', {form:form})



    #     form.board_detail = data.board_detail
    #     print(form.board_detail,'ddddddddddddddddddddddddddddddddddd')
    #     type = form.cleaned_data['type']
    #     bus_section = form.cleaned_data['bus_section']
    #     module_code = form.cleaned_data['module_code']
    #     quantity = form.cleaned_data['quantity']
    #     revision = form.cleaned_data['revision']
    #     description = form.cleaned_data['description']
    #     quantity2 = form.cleaned_data['quantity2']
    #     quantity3 = form.cleaned_data['quantity3']
    #     quantity4 = form.cleaned_data['quantity4']
    #     quantity5 = form.cleaned_data['quantity5']
    #     total_quantity = quantity + quantity2 + quantity3 + quantity4 + quantity5
    # # p = models.ModuleDetails(board_detail=form.board_detail, type=type, bus_section=bus_section, tender_id=tender_id_data,
    # #                          module_code=module_code, quantity=quantity,total_quantity=total_quantity,
    # #                          revision=revision, description=description, quantity2=quantity2,
    # #                          quantity3=quantity3, quantity4=quantity4, quantity5=quantity5)
    # # print(p,'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    # # p.save()
    #     dataa.save()




@flow_start_view
def add_module_list(request, **kwargs):
    tender_i = request.session.get('id_tender')
    print(tender_i, '3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')
    # cursor = connection.cursor()
    # cursor.execute("SELECT 'board_code' FROM models.BoardDetails WHERE tender_id = 1098")
    # result = cursor.fetchall()
    # print(result, 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    queryset = models.BoardDetails.objects.select_related().filter(tender_id=tender_i)
    print(queryset,'sssssssssw22222222')
    print(models.BoardDetails.objects.filter(tender_id=tender_i),'8888888888888888888888888888888888888')
    request.activation.prepare(request.POST or None)
    form = forms.ModuleDetailForm(request.POST or None)
    if form.is_valid():
        # for i in queryset:
        #     print(i, 'iiiiiiiiiiiiiiiiiiiiii')
        #     board_detail = form.cleaned_data['i']
        #     print(board_detail, 'pppppppppppppppppppppppppppppppppp')
        board_detail =form.cleaned_data['board_detail']
        print(board_detail,'wwww222222222222222222222222222222222222')
        type = form.cleaned_data['type']
        bus_section = form.cleaned_data['bus_section']
        module_code = form.cleaned_data['module_code']
        quantity = form.cleaned_data['quantity']
        revision = form.cleaned_data['revision']
        description = form.cleaned_data['description']
        quantity2 = form.cleaned_data['quantity2']
        quantity3 = form.cleaned_data['quantity3']
        quantity4 = form.cleaned_data['quantity4']
        quantity5 = form.cleaned_data['quantity5']
        total_quantity = quantity + quantity2 + quantity3 + quantity4 + quantity5
        p = models.ModuleDetails(board_detail=board_detail, type=type, bus_section=bus_section, tender_id=tender_i,
                                 module_code=module_code, quantity=quantity,total_quantity=total_quantity,
                                 revision=revision, description=description, quantity2=quantity2,
                                 quantity3=quantity3, quantity4=quantity4, quantity5=quantity5)
        p.save()
        return redirect('.')
    elif request.POST:
        return redirect(get_next_task_url(request, request.activation.process))
    form = forms.ModuleDetailForm()
    incoming_data = models.ModuleDetails.objects.filter(tender_id=tender_i, type='incoming')
    outgoing_data = models.ModuleDetails.objects.filter(tender_id=tender_i, type='outgoing')
    coupler_data = models.ModuleDetails.objects.filter(tender_id=tender_i, type='bus_coupler')
    return render(request, 'app/app/add_module.html', {
        'form': form,
        'incoming_data': incoming_data,
        'outgoing_data': outgoing_data,
        'coupler_data': coupler_data,
        'activation': request.activation
    })
# #
# @flow_start_view
# def add_module_list(request, **kwargs):
#     tender_i = request.session.get('id_tender')
#     print(tender_i, '3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')
#     # cursor = connection.cursor()
#     # cursor.execute("SELECT 'board_code' FROM models.BoardDetails WHERE tender_id = 1098")
#     # result = cursor.fetchall()
#     # print(result, 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
#     # queryset = models.BoardDetails.objects.select_related().filter(tender_id=tender_i)
#     # print(queryset,'sssssssssw22222222')
#     # print(models.BoardDetails.objects.filter(tender_id=tender_i),'8888888888888888888888888888888888888')
#     request.activation.prepare(request.POST or None)
#     form = forms.ModuleDetailForm(request.POST or None)
#     if form.is_valid():
#         # for i in queryset:
#         #     print(i, 'iiiiiiiiiiiiiiiiiiiiii')
#         #     board_detail = form.cleaned_data['i']
#         #     print(board_detail, 'pppppppppppppppppppppppppppppppppp')
#         board_detail =tender_i
#         print(board_detail,'wwww222222222222222222222222222222222222')
#         type = form.cleaned_data['type']
#         bus_section = form.cleaned_data['bus_section']
#         module_code = form.cleaned_data['module_code']
#         quantity = form.cleaned_data['quantity']
#         revision = form.cleaned_data['revision']
#         description = form.cleaned_data['description']
#         quantity2 = form.cleaned_data['quantity2']
#         quantity3 = form.cleaned_data['quantity3']
#         quantity4 = form.cleaned_data['quantity4']
#         quantity5 = form.cleaned_data['quantity5']
#         total_quantity = quantity + quantity2 + quantity3 + quantity4 + quantity5
#         p = models.ModuleDetails(board_detail=tender_i, type=type, bus_section=bus_section, tender_id=tender_i,
#                                  module_code=module_code, quantity=quantity,total_quantity=total_quantity,
#                                  revision=revision, description=description, quantity2=quantity2,
#                                  quantity3=quantity3, quantity4=quantity4, quantity5=quantity5)
#         p.save()
#         return redirect('.')
#     elif request.POST:
#         return redirect(get_next_task_url(request, request.activation.process))
#     form = forms.ModuleDetailForm()
#     incoming_data = models.ModuleDetails.objects.filter(tender_id=tender_i, type='incoming')
#     outgoing_data = models.ModuleDetails.objects.filter(tender_id=tender_i, type='outgoing')
#     coupler_data = models.ModuleDetails.objects.filter(tender_id=tender_i, type='bus_coupler')
#     return render(request, 'app/app/add_module.html', {
#         'form': form,
#         'incoming_data': incoming_data,
#         'outgoing_data': outgoing_data,
#         'coupler_data': coupler_data,
#         'activation': request.activation
#     })


def module_form_view(request, **kwargs):
    new_item = get_object_or_404(models.ModuleDetails, pk=kwargs['pk'])
    print(new_item, "new item")
    queryset = models.ModuleDetails.objects.select_related().filter(pk=kwargs['pk'])
    print(queryset,'dddddddddd')
    for i in queryset:
        data = queryset.update(board_detail=i.board_detail, type=i.type, bus_section=i.bus_section,
                               module_code=i.module_code, quantity=i.quantity,
                               revision=i.revision, description=i.description, quantity2=i.quantity2,
                               quantity3=i.quantity3, quantity4=i.quantity4, quantity5=i.quantity5)
    form = forms.ModuleDetailForm(request.POST or None, instance=new_item)
    print(request.method,'pppppppp')
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('.')
    context = {
        'form': form,
    }
    return render(request, 'app/app/module_form.html', context)
#
#
# # @flow_start_view
# def add_component_list(request, **kwargs):
#     tender_id_data = request.session.get('tend_id')
#     # new_item = get_object_or_404(models.ModuleDetails, pk=kwargs['pk'])
#     # print(new_item, "new item3333333333333333333333333333333")
#     # print(tender_id_data,'tender--------------------')
#     queryset = models.ModuleDetails.objects.filter(pk=kwargs['pk'])
#     print(queryset,'dddddddddd222222222222233333333333333333333444444444444444444444444444444444')
#     # for i in queryset:
#     #     print(i.module_code, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#     #     data = request.POST.get(i.module_code)
#     # data = models.ComponentDetails.objects.filter(tender_id = tender_id_data).create(module_detail=i.module_code)
#     #     # data = models.ComponentDetails.update(module_detail=i.module_code)
#     #     print(data, 'ssssssssss')
#     form = forms.ComponentDetailForm(request.POST or None)
#     print(form, '22222222222222222')
#     print(request.method, 'rrrrrrrrrrrrrrrrrrrrrr')
#     # request.activation.prepare(request.POST or None)
#     print(form.is_valid(), '33333333333333333333333')
#     if form.is_valid():
#         form_data = form.save(commit=False)
#         print(form_data,'eeeeeeeeeeeeeeeeeeeeeeeeeee')
#         module_detail = request.GET.get(queryset)
#         print(module_detail,'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
#         # if module_detail:
#         #     print(module_detail,'xxxxxxxxxxxxxxxxxxxx')
#         # else:
#         #     print(module_detail.errors,'===========================')
#         component_id = form.cleaned_data['component_id']
#         description = form.cleaned_data['description']
#         quantity = form.cleaned_data['quantity']
#         print(quantity, 'quantityffffffffffffffffffff')
#         p = models.ComponentDetails(module_detail=module_detail, component_id=component_id, quantity=quantity,
#                                     description=description, tender_id=tender_id_data)
#         print(p, 'ddddddddddddddddddddddddddd')
#         p.save()
#         return redirect('.')
#     else:
#         print(form.errors, '444444444444444444444444444')
#     form = forms.ComponentDetailForm()
#     component_data = models.ComponentDetails.objects.filter(tender_id=tender_id_data)
#     return render(request, 'app/app/add_component.html', {
#         'form': form,
#         'component_data': component_data,
#         # 'activation': request.activation
#     })
#     # def get_context_data(self, **kwargs)
#     #     """ get_context_data let you fill the template context """
#     #     context = super(models.ComponentDetails, self).get_context_data(**kwargs)
#     #     # Get Related publishers
#     #     context['publishers'] = self.object.publishers.filter(is_active=True)
#     #     return context
#


def component_form_view(request, **kwargs):
    new_item = get_object_or_404(models.ComponentDetails, pk=kwargs['pk'])
    print(new_item, "new item")
    queryset = models.ComponentDetails.objects.select_related().filter(pk=kwargs['pk'])
    print(queryset,'dddddddddd')
    for i in queryset:
        data = queryset.update(board_detail=i.board_detail, component_id=i.component_id, quantity=i.quantity,
                                 description=i.description)
        print(data,'ssssssssss')
    form = forms.ComponentDetailForm(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('.')
    context = {
        'form': form,
    }
    return render(request, 'app/app/component_form.html', context)


def add_component_list(request, **kwargs):
    print(kwargs['pk'],'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
    new_item = get_object_or_404(models.ModuleDetails, pk=kwargs['pk'])
    print(new_item.board_detail, "new itemrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    new_item.pk = None
    board_detail = new_item.board_detail
    print(board_detail,'ddddddddddddddddddddddddddddddd')
    tender_id_data = request.session.get('id_tender')
    print(tender_id_data,'ooooooooooooooooooo')
    queryset = models.ModuleDetails.objects.select_related().filter(pk=kwargs['pk'])
    print(queryset,'dddddddddd')
    form = forms.ComponentDetailForm(request.POST or None, instance=new_item)
    if form.is_valid():
        # form_data = form.save(commit=False)
        board_detail = board_detail
        print(board_detail, 'oooooooooooooooooooooooooooooo')
        # form_data.tender_id = tender_id_data
        component_id = form.cleaned_data['component_id']
        description = form.cleaned_data['description']
        quantity = form.cleaned_data['quantity']
        print(quantity, 'quantityffffffffffffffffffff')
        p = models.ComponentDetails(board_detail=board_detail, component_id=component_id, quantity=quantity,
                                    description=description, tender_id=tender_id_data)
        print(p, 'ddddddddddddddddddddddddddd')
        p.save()
        return redirect('.')
    context = {
        'form': form,
    }
    # form = forms.ComponentDetailForm()
    # component_data = models.ComponentDetails.objects.filter(tender_id=tender_id_data)
    # print(component_data,'oooooooooooeeeeeeeeeeeeeeeeeeeeeeeeeee')
    return render(request, 'app/app/add_component_copy.html', context)
                  # {'component_data': component_data})