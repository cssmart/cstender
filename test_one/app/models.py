from django.db import models
from viewflow.models import Process
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
import datetime


# class BoardType(models.Model):
#     stand_or_non = models.CharField(choices=[('standard', 'STANDARD'), ('nonstandard', 'NONSTANDARD')],
#                                     max_length=100, default='')
#     indoor_or_outdoor = models.CharField(choices=[('indoor', 'INDOOR'), ('outdoor', 'OUTDOOOR')],
#                                          max_length=100, default='')
#     mcc_or_nonstan = models.CharField(choices=[('mcc code', 'MCC CODE'), ('non_stan code', 'NON_STAN CODE')],
#                                       max_length=100, default='')
#
#     def __str__(self):
#         return self.stand_or_non + ", " + self.indoor_or_outdoor + ", " + self.mcc_or_nonstan
#
#
# class AddBoard(models.Model):
#
#     board_code = models.CharField(max_length=100)
#     board_desc = models.CharField(max_length=100)
#     board_qty = models.IntegerField()
#     board_type = models.ForeignKey(BoardType, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.board_code + "," + self.board_desc


class TenderProcess(Process):

    # record_id = models.CharField(primary_key=True, null=False, max_length=15, default="")
    # last_updated_by = models.CharField(max_length=50, default="")
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=20, blank=True)
    customer_name = models.CharField(max_length=250, unique=True)
    project_name = models.CharField(max_length=250, unique=True)
    approved = models.BooleanField(default=False)
    panel_sheet = models.CharField(choices=[('hrc', 'HRC'), ('crc', 'CRC')], max_length=3)
    epoxy_paint = models.BooleanField(default=False)
    base_frame = models.BooleanField(default=False)
    gland_comp = models.CharField(choices=[('single', 'Single'), ('double', 'Double')], max_length=7)
    bus_bar = models.CharField(choices=[('alum.', 'Alum.'), ('copper', 'Copper')], max_length=7)
    pvc_sleeves = models.BooleanField(default=False)
    htc_bolt = models.BooleanField(default=False)
    shutter_mcc = models.BooleanField(default=False)
    shrouds = models.BooleanField(default=False)
    board_code = models.CharField(max_length=100, default="cs_101")
    stand_or_non = models.CharField(choices=[('standard', 'STANDARD'), ('nonstandard', 'NONSTANDARD')],
                                    max_length=100, default="")
    indoor_or_outdoor = models.CharField(choices=[('indoor', 'INDOOR'), ('outdoor', 'OUTDOOOR')],
                                         max_length=100, default="")
    mcc_or_nonstan = models.CharField(choices=[('mcc code', 'MCC CODE'), ('non_stan code', 'NON_STAN CODE')],
                                      max_length=100, default="")
    board_desc = models.CharField(max_length=100, default="desc_1001")
    board_qty = models.IntegerField(default=0)
    mcc_description = models.CharField(max_length=100, blank=True)
    hori_bus_bar_desc = models.CharField(max_length=100, blank=True, help_text='Amps')
    control_bus_bar_qty = models.IntegerField(default=0)
    front_access_panel = models.BooleanField(default=True)
    phase = models.CharField(choices=[('D', 'D'), ('T', 'T'),('N','N')], default="",  max_length=10,
                        help_text='D=DP/T=TP/N=TPN')
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", default=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_updated_by", default=True)
    owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE)
    # board_details = models.ForeignKey(AddBoard, null=True, on_delete=models.CASCADE)

    def __str__(self):

        return self.customer_name