from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from . import views, models, forms
from django.contrib.auth.models import User


@frontend.register
class TenderFlow(Flow):
    process_class = models.TenderDataProcess

    tender_process = flow.Start(
        views.FirstTenderView,
        task_title="Tender Details"
    ).Next(this.board_list_data)

    board_list_data = flow.View(
        views.add_board_summary,
        task_title="Board List View"
    ).Next(this.module_list_data)

    board_form = flow.Start(
        views.add_board_detail,
        task_title="Board View"
    ).Next(this.module_list_data)

    module_list_data = flow.Start(
        views.add_module_list,
        task_title="Module List"
    ).Next(this.component_form)

    component_form = flow.Start(
        views.add_component_list,
        task_title="Component Form"
    ).Next(this.component_form_data)
    component_form_data = flow.Start(
        views.component_form_view,
        task_title="Component Form View"
    ).Next(this.end)

    end = flow.End()