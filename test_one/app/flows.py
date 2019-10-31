from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import TenderProcess
# from .models import TenderProcess, AddBoard,BoardType
from django.contrib.auth.models import User


@frontend.register
class TenderCreationFlow(Flow):
    process_class = TenderProcess

    tender_creation = (
        flow.Start(
            CreateProcessView,
            fields=["code", "customer_name", "project_name"]
            # task_title="Tender Creation"
        ).Permission(
            auto_create=True
            # obj=lambda activation: activation.process.createdby
        # ).Permission(
        # lambda act: act.process.created_by
        ).Next(this.tendor_body)
    )
    tendor_body = (
        flow.View(
            UpdateProcessView,
            fields=["panel_sheet", "gland_comp", "bus_bar", "pvc_sleeves", "htc_bolt",
                    "shutter_mcc", "shrouds", "epoxy_paint", "base_frame"],
            task_title="Tender Body"
        ).Permission(
            auto_create=True
        ).Next(this.board_details)
    )
    board_details = (
        flow.View(
            UpdateProcessView,
            fields=['board_code', 'stand_or_non','indoor_or_outdoor','mcc_or_nonstan','board_desc','board_qty',
                    'mcc_description','hori_bus_bar_desc','control_bus_bar_qty','front_access_panel','phase'],
            task_title="Board Deatils"
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )
    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"],
            task_title="Approval Process"
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    # add_board = flow.View(
    #     CreateProcessView,
    #     model=AddBoard,
    #     fields=[
    #         'board_code', 'board_desc', 'board_qty',
    #
    #     ],
    #     task_description='Add Board8'
    # ).Next(this.end)
    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.created_by)
