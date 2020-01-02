from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url
from . import forms, models
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
import datetime


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


# def add_board_summary(request, **kwargs):
#     # new_item = get_object_or_404(models.BOARDS,  pk=kwargs['pk'])
#     # print(new_item)
#     # queryset = models.BOARDS.objects.select_related().filter(pk=kwargs['pk'])
#     # print(queryset, 'ssssssssssssssssssssssssssssssssssssssssssss')
#     form = forms.BoardDetailForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect(' ')
#     return render(request, 'app/app/list_board2.html', {'form':form})

def master_boards_details(request, **kwargs):
    print(request, 'uuuuuuuuuuuuuuuuuuuuuuuuuuu')
    data = models.BOARDS.objects.all()
    for i in data:
        print(i.id, 'ppwwwwwwwwwww')
    new_item = get_object_or_404(models.BOARDS, pk=i.id)
    tender_id_data = request.session.get('tend_id')
    request.session['idtender'] = tender_id_data
    print(request.session['idtender'], 'ffsssssssssssssssssss')
    print(tender_id_data, 'ddddddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    master_boards = models.BOARDS.objects.select_related().all()
    print(master_boards, 'ddddddddddddddddddddd')
    return render(request, 'app/app/master_boards.html', {'master_boards': master_boards})


# from django.db import connection
# @flow_view
def add_board_summary(request, **kwargs):
    print(request, 'uuuuuuuuuuuuuuuuuuuuuuuuuuu')
    data = models.BOARDS.objects.all()
    for i in data:
        print(i.id,'ppwwwwwwwwwww')
    new_item = get_object_or_404(models.BOARDS, pk=i.id)
    board_code = new_item.board_code
    board_desc = new_item.board_desc
    tender_id_data = request.session.get('idtender')
    print(tender_id_data, 'iiiiiiiiiiiiiiiiiiiiiiiiiiii')
    form = forms.BoardDetailForm(request.POST or None, instance=new_item)
    print(request.method,'ssssssssssssssssssssss')
    print(form.is_valid(), 'pppppppppppppppppppppppppppp')
    if form.is_valid():
        form_data = form.save(commit= False)
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
    else:
        print(form.errors, '9999999999999999999999999999999999999999999999999999999999999999')
    # elif request.POST:
    #     return redirect(get_next_task_url(request, request.activation.process))

    form = forms.BoardDetailForm()
    model_data = models.BoardDetails.objects.filter(tender_id=tender_id_data)
    context = {
    'form':form,
     'model_data':model_data
    }
    return render(request, 'app/app/list_board.html', context)


def add_board_from_master(request, **kwargs):
    newitem = get_object_or_404(models.BOARDS, pk=kwargs['pk'])
    print(newitem, 'oooooooooooooooooooooooooooooooo')
    print(newitem.pk,'ssssssssssswwwwwwwwwwwwwww')
    queryset = models.BOARDS.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        board_code = i.board_code
        print(board_code, 'iiiiiiiiiiiiiiiiiiiii')
        board_desc = i.board_desc
    tender_id_data = request.session.get('idtender')
    print(tender_id_data, 'ooooe 333333333333333333')
    print(queryset, 'owwwwwwwwwwwwwwwwwwwwwwwwwwww 3333333333333333333333333333333')
    form = forms.BoardlistForm(request.POST or None, instance=newitem)
    print(request.method, 'pe3333333333333333333')
    print(form.is_valid(), 'wwwwwwwwwwwwwwwwwww')
    if form.is_valid():
        board_code = board_code
        board_desc =board_desc
        stand_or_non = form.cleaned_data['stand_or_non']
        indoor_or_outdoor = form.cleaned_data['indoor_or_outdoor']
        mcc_or_nonstan = form.cleaned_data['mcc_or_nonstan']
        board_qty = form.cleaned_data['board_qty']
        mcc_description = form.cleaned_data['mcc_description']
        hori_bus_bar_desc = form.cleaned_data['hori_bus_bar_desc']
        control_bus_bar_qty = form.cleaned_data['control_bus_bar_qty']
        front_access_panel = form.cleaned_data['front_access_panel']
        phase = form.cleaned_data['phase']
        datasave = models.BoardDetails(board_code=board_code, board_desc=board_desc, tender_id=tender_id_data,
                                       stand_or_non=stand_or_non, indoor_or_outdoor=indoor_or_outdoor,
                                       mcc_or_nonstan=mcc_or_nonstan, board_qty=board_qty,phase=phase,
                                       mcc_description=mcc_description,control_bus_bar_qty=control_bus_bar_qty,
                                       hori_bus_bar_desc=hori_bus_bar_desc, front_access_panel=front_access_panel)
        datasave.save()
        print(datasave, 'pwwwwwwwwwwww222222222222222222222')
        return redirect('.')
    else:
        print(form.errors, 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    model_data = models.BoardDetails.objects.filter(tender_id=tender_id_data)
    context = {
        'tender_id': tender_id_data,
        'form':form,
        'model_data':model_data
    }
    # form1 = forms.BoardDetailForm()
    return render(request, 'app/app/add_board_copy.html', context)


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


def delete_board(request,**kwargs):
    raw_del = models.BoardDetails.objects.filter(pk=kwargs['pk'])
    if raw_del:
        raw_del.delete()
        messages.success(request, 'Entry was successfully removed!')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META['HTTP_REFERER'])


def add_module_list(request, **kwargs):
    new_item = get_object_or_404(models.BoardDetails, pk=kwargs['pk'])
    board_desc =new_item.board_desc
    board_code =new_item.board_code
    tender_id = new_item.tender_id
    form = forms.ModuleDetailForm(request.POST or None, instance=new_item)
    if form.is_valid():
        bus_section = form.cleaned_data['bus_section']
        module_type = form.cleaned_data['module_type']
        module_code = form.cleaned_data['module_code']
        quantity = form.cleaned_data['quantity']
        revision = form.cleaned_data['revision']
        module_desc =form.cleaned_data['module_desc']
        quantity2 = form.cleaned_data['quantity2']
        quantity3 = form.cleaned_data['quantity3']
        quantity4 = form.cleaned_data['quantity4']
        quantity5 = form.cleaned_data['quantity5']
        total_quantity = quantity + quantity2 + quantity3 + quantity4 + quantity5
        p = models.ModuleDetails(board_code=board_code,board_id=new_item.id, board_desc=board_desc, module_type=module_type,
                                 tender_id=tender_id, module_code=module_code, quantity=quantity, revision=revision,
                                 module_desc=module_desc, quantity2=quantity2, quantity3=quantity3, quantity4=quantity4,
                                 quantity5=quantity5, total_quantity=total_quantity, bus_section=bus_section)
        p.save()
        return redirect(".")
    incoming_data = models.ModuleDetails.objects.filter(tender_id=tender_id, module_type='incoming', board_id =kwargs['pk'])
    outgoing_data = models.ModuleDetails.objects.filter(tender_id=tender_id, module_type='outgoing', board_id =kwargs['pk'])
    coupler_data = models.ModuleDetails.objects.filter(tender_id=tender_id, module_type='bus_coupler', board_id =kwargs['pk'])
    context = {
        'form': form,
        'incoming_data': incoming_data,
        'outgoing_data': outgoing_data,
        'coupler_data': coupler_data,
    }
    return render(request, 'app/app/add_module.html', context)


def delete_module(request,**kwargs):
    raw_del = models.ModuleDetails.objects.filter(pk=kwargs['pk'])
    if raw_del:
        raw_del.delete()
        messages.success(request, 'Entry was successfully removed!')
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META['HTTP_REFERER'])


def module_form_view(request, **kwargs):
    new_item = get_object_or_404(models.ModuleDetails, pk=kwargs['pk'])
    queryset = models.ModuleDetails.objects.select_related().filter(pk=kwargs['pk'])
    for i in queryset:
        data = queryset.update(board_code=i.board_code, board_desc=i.board_desc, module_type=i.module_type, bus_section=i.bus_section,
                               module_code=i.module_code, quantity=i.quantity,
                               revision=i.revision, module_desc=i.module_desc, quantity2=i.quantity2,
                               quantity3=i.quantity3, quantity4=i.quantity4, quantity5=i.quantity5)
    form = forms.ModuleDetailForm(request.POST or None, instance=new_item)
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('.')
    context = {
        'form': form,
    }
    return render(request, 'app/app/module_form.html', context)


def component_form_view(request, **kwargs):
    new_item = get_object_or_404(models.ComponentDetails, pk=kwargs['pk'])
    queryset = models.ComponentDetails.objects.select_related().filter(pk=kwargs['pk'])
    print(queryset)
    for i in queryset:
        data = queryset.update(board_detail=i.board_detail, component_id=i.component_id,
                               component_quantity=i.component_quantity, component_desc=i.component_desc)
        print(data)
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
    new_item = get_object_or_404(models.ModuleDetails, pk=kwargs['pk'])
    module_id = new_item.id
    board_code = new_item.board_code
    board_desc = new_item.board_desc
    module_code = new_item.module_code
    module_desc = new_item.module_desc
    tender_id = new_item.tender_id
    queryset = models.ModuleDetails.objects.select_related().filter(pk=kwargs['pk'])
    form = forms.ComponentDetailForm(request.POST or None, instance=new_item)
    if form.is_valid():
        module_code=module_code
        module_desc=module_desc
        board_code = board_code
        board_desc = board_desc
        component_id = form.cleaned_data['component_id']
        component_desc = form.cleaned_data['component_desc']
        component_quantity = form.cleaned_data['component_quantity']
        p = models.ComponentDetails(board_code=board_code,board_desc=board_desc, module_desc=module_desc,module_id=module_id,
                                    component_id=component_id, component_quantity=component_quantity,module_code=module_code,
                                    component_desc=component_desc, tender_id=tender_id)
        p.save()
        return redirect('.')
    component_data = models.ComponentDetails.objects.filter(tender_id=tender_id, module_id=module_id)
    context = {
        'form': form,
        'component_data': component_data
    }
    return render(request, 'app/app/add_component_copy.html', context)


def delete_component(request, **kwargs):
    raw_del = models.ComponentDetails.objects.filter(pk=kwargs['pk'])
    if raw_del:
        raw_del.delete()
        messages.success(request, 'Component Entry was successfully removed!')
        return redirect(request.META['HTTP_REFERER'])



# from django.db import connection
# @flow_view
# def add_board_summary(request, **kwargs):
#     print(request,'uuuuuuuuuuuuuuuuuuuuuuuuuuu')
#     # new_item = get_object_or_404(models.BOARDS,  pk=kwargs['pk'])
#     # queryset = models.BOARDS.objects.select_related().filter(pk=kwargs['pk'])
#     # print(queryset,'ssssssssssssssssssssssssssssssssssssssssssss')
#     board_code = request.POST.get('board_code')
#     tender_id_data = request.session.get('tend_id')
#     print(tender_id_data)
#     request.session['id_tender'] = tender_id_data
#     request.activation.prepare(request.POST or None)
#     form = forms.BoardDetailForm(request.POST or None)
#     board_form = forms.BoardForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             board_code = form.cleaned_data['board_code']
#             board_desc = form.cleaned_data['board_desc']
#             stand_or_non = form.cleaned_data['stand_or_non']
#             indoor_or_outdoor = form.cleaned_data['indoor_or_outdoor']
#             mcc_or_nonstan = form.cleaned_data['mcc_or_nonstan']
#             board_qty = form.cleaned_data['board_qty']
#             mcc_description = form.cleaned_data['mcc_description']
#             hori_bus_bar_desc = form.cleaned_data['hori_bus_bar_desc']
#             control_bus_bar_qty = form.cleaned_data['control_bus_bar_qty']
#             front_access_panel = form.cleaned_data['front_access_panel']
#             phase = form.cleaned_data['phase']
#             board_save = models.BoardDetails(board_code=board_code, board_desc=board_desc, tender_id=tender_id_data,
#                                              stand_or_non=stand_or_non, indoor_or_outdoor=indoor_or_outdoor,
#                                              mcc_or_nonstan=mcc_or_nonstan, board_qty=board_qty, mcc_description=mcc_description,
#                                              hori_bus_bar_desc=hori_bus_bar_desc, front_access_panel=front_access_panel,
#                                              phase=phase, control_bus_bar_qty=control_bus_bar_qty)
#             board_save.save()
#             return redirect('.')
#     if request.method == 'POST':
#         if board_form.is_valid():
#             board_code = request.POST.get('board_code')
#             queryset = models.BOARDS.objects.filter(BRD_CODE=board_code).distinct('BRD_CODE')
#             if queryset:
#                 for i in queryset:
#                     p = models.BoardDetails(board_code=board_code, board_desc=i.BRD_DESC, tender_id=tender_id_data)
#                     p.save()
#             return redirect('.')
#         else:
#             print(form.errors)
#     elif request.POST:
#         return redirect(get_next_task_url(request, request.activation.process))
#     board_form = forms.BoardForm()
#     form = forms.BoardDetailForm()
#     model_data = models.BoardDetails.objects.filter(tender_id=tender_id_data)
#     return render(request, 'app/app/list_board.html', {
#         'tender_id':tender_id_data,
#         'form': form,
#         'board_form':board_form,
#         'model_data': model_data,
#         'activation': request.activation
#     })