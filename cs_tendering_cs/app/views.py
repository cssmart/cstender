from django.shortcuts import render
from django.shortcuts import render, redirect
from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url
from . import forms, models
from django.shortcuts import render_to_response
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from formtools.wizard.views import SessionWizardView
from django.template import RequestContext
from django.db import connection, transaction


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


@flow_view
def add_board_summary(request, **kwargs):
    tender_id_data = request.session.get('tend_id')
    request.activation.prepare(request.POST or None)
    form = forms.BoardDetailForm(request.POST or None)

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

        p = models.BoardDetails(board_code=board_code, board_desc=board_desc, tender_id=tender_id_data,
                                stand_or_non=stand_or_non, indoor_or_outdoor=indoor_or_outdoor,
                                mcc_or_nonstan=mcc_or_nonstan, board_qty=board_qty, mcc_description=mcc_description,
                                hori_bus_bar_desc=hori_bus_bar_desc, front_access_panel=front_access_panel,
                                phase=phase, control_bus_bar_qty=control_bus_bar_qty)
        p.save()
        return redirect('.')
    elif request.POST:
        return redirect(get_next_task_url(request, request.activation.process))
    form = forms.BoardDetailForm()
    model_data = models.BoardDetails.objects.filter(tender_id=tender_id_data)
    return render(request, 'app/app/list_board.html', {
        'form': form,
        'model_data': model_data,
        'activation': request.activation
    })


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


@flow_start_view
def add_module_list(request, **kwargs):
    tender_id_data = request.session.get('tend_id')
    request.activation.prepare(request.POST or None)
    form = forms.ModuleDetailForm(request.POST or None)

    if form.is_valid():
        board_detail = form.cleaned_data['board_detail']
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
        total_quantity = quantity + quantity2+quantity3+quantity4+quantity5
        p = models.ModuleDetails(board_detail=board_detail, type=type, bus_section=bus_section, tender_id=tender_id_data,
                                 module_code=module_code, quantity=quantity,total_quantity=total_quantity,
                                 revision=revision, description=description, quantity2=quantity2,
                                 quantity3=quantity3, quantity4=quantity4, quantity5=quantity5)
        p.save()
        return redirect('.')
    elif request.POST:
        return redirect(get_next_task_url(request, request.activation.process))
    form = forms.ModuleDetailForm()
    incoming_data = models.ModuleDetails.objects.filter(tender_id=tender_id_data, type='incoming')
    outgoing_data = models.ModuleDetails.objects.filter(tender_id=tender_id_data, type='outgoing')
    coupler_data = models.ModuleDetails.objects.filter(tender_id=tender_id_data, type='bus_coupler')
    return render(request, 'app/app/add_module.html', {
        'form': form,
        'incoming_data': incoming_data,
        'outgoing_data': outgoing_data,
        'coupler_data': coupler_data,
        'activation': request.activation
    })


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
    if form.is_valid():
        form_data = form.save(commit=False)
        form_data.save()
        return redirect('.')
    context = {
        'form': form,
    }
    return render(request, 'app/app/module_form.html', context)


@flow_start_view
def add_component_list(request, **kwargs):
    tender_id_data = request.session.get('tend_id')
    request.activation.prepare(request.POST or None)
    form = forms.ComponentDetailForm(request.POST or None)
    print(form,'22222222222222222')
    print(form.is_valid(),'33333333333333333333333')
    if form.is_valid():
        module_detail = form.cleaned_data['module_detail']
        if module_detail:
            print(module_detail,'xxxxxxxxxxxxxxxxxxxx')
        else:
            print(module_detail.errors,'===========================')

        component_id = form.cleaned_data['component_id']
        description = form.cleaned_data['description']
        quantity = form.cleaned_data['quantity']
        print(quantity, 'quantityffffffffffffffffffff')
        p = models.ComponentDetails(module_detail=module_detail, component_id=component_id, quantity=quantity,
                                 description=description,tender_id=tender_id_data)
        print(p,'ddddddddddddddddddddddddddd')
        p.save()
        return redirect('.')
    else:
        print(form.errors,'444444444444444444444444444')
    form = forms.ComponentDetailForm()
    component_data = models.ComponentDetails.objects.filter(tender_id=tender_id_data)
    return render(request, 'app/app/add_component.html', {
        'form': form,
        'component_data': component_data,
        'activation': request.activation
    })


def component_form_view(request, **kwargs):
    new_item = get_object_or_404(models.ComponentDetails, pk=kwargs['pk'])
    print(new_item, "new item")
    queryset = models.ComponentDetails.objects.select_related().filter(pk=kwargs['pk'])
    print(queryset,'dddddddddd')
    for i in queryset:
        data = queryset.update(module_detail=i.module_detail, component_id=i.component_id, quantity=i.quantity,
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




















#
# def add_board_detail(request, **kwargs):
#     new_item = get_object_or_404(models.BoardDetails,  pk=kwargs['pk'])
#     print(new_item, "new item====================")
#     if request.method == 'POST':
#         form = forms.BoardDetailForm(request.POST, instance=new_item)
#         print(form.is_valid(),'sssssssssssssssssssssssssssssssss')
#         if form.is_valid():
#             data = form.save(commit=False)
#
#             print(data,'1111111111111111111111111111')
#             data.board_code = 'form.board_code'
#             print( new_item.board_code, 'dddddddddddddddddd')
#
#             form.save()
#             # if not request.is_ajax():
#             #     # reload the page
#             #     next = request.META['PATH_INFO']
#             # return HttpResponseRedirect(next)
#             return redirect('/done')
#             # if is_ajax(), we just return the validated form, so the modal will close
#     # else:
#     #     data = {"board_code": new_item.board_code
#     #             }
#     #     print(data,'dddddddddddd22222222222222222')
#     #     # form = AdvertForm(initial=data)
#     #
#     form = forms.BoardDetailForm(instance=new_item)
#
#     return render(request, 'app/app/board_form.html', {
#         # 'object': object,
#         'form': form,
#     })



    # new_item = models.BoardDetails.objects.update_or_create(pk=kwargs['pk'],
    #                                        defaults={
    #                                            'board_detail': 'board_detail',
    #                                        })
    # # models.BoardDetails.objects.all().update(blog=new_item)
    # # new_item.board_code ="dddddddddd"
    # new_item.pk = None
    # # data = models.BoardDetails.objects.filter(pk='122').update(board_code="11111111")
    # form = forms.BoardDetailForm(request.POST or None, instance=new_item)
    #
    # # print(data, 'dddddeeeeeeeeeeee')
    # print(form.is_valid(),'fffffffffffffffffffffff')
    # if form.is_valid():
    #     board_code = form.cleaned_data['board_code']
    #     data = models.BoardDetails.objects.update(board_code=board_code)
    #     # board_detail = new_item['board_code']
    #     # print(board_detail,'ddddddddddddddddddddddddddddd')
    #     # data = models.ModuleDetails(board_detail=board_detail)
    #     data.save()
    # context = {
    #         'form':form,
    #     }
    # return render(request, 'app/app/board_form.html',context)