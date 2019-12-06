from django.db import models
from viewflow.models import Process
from django.contrib.auth.models import User


class TenderDataDetails(models.Model):

    tender_code = models.CharField(max_length=20)
    tender_version = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=250, blank=False)
    project_name = models.CharField(max_length=250, blank=False)
    # created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", default=True)
    # last_updated = models.DateTimeField(auto_now=True, null=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_updated_by", default=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class BodyDetails(models.Model):
    # id = models.IntegerField(primary_key=True)
    tender_id= models.CharField(max_length=20, null=True, blank=False)
    # tender_version = models.CharField(max_length=20)
    panel_sheet = models.CharField(choices=[('hrc', 'HRC'), ('crc', 'CRC')], max_length=3)
    epoxy_paint = models.BooleanField(default=False)
    shrouts = models.BooleanField(default=False)
    htc_bolt = models.BooleanField(default=False)
    shutter_mcc = models.BooleanField(default=False)
    bus_bar = models.CharField(choices=[('alum.', 'Alum.'), ('copper', 'Copper')], max_length=7)
    pvc_sleeves = models.BooleanField(default=False)
    base_frame = models.BooleanField(default=False)
    gland_comp = models.CharField(choices=[('single', 'Single'), ('double', 'Double')], max_length=7)

    def __str__(self):
        return str(self.tender_id)


class BoardDetails(models.Model):
    # id = models.IntegerField(primary_key=True)
    # tender = models.ForeignKey(TenderDataDetails, on_delete=models.CASCADE,  default=True)
    tender_id= models.CharField(max_length=20, null=True, blank=False)
    # tender_version = models.CharField(max_length=20)
    board_code = models.CharField(max_length=100, blank=False)
    stand_or_non = models.CharField(choices=[('standard', 'STANDARD'), ('nonstandard', 'NONSTANDARD')],
                                    max_length=100, default="")
    indoor_or_outdoor = models.CharField(choices=[('indoor', 'INDOOR'), ('outdoor', 'OUTDOOOR')],
                                         max_length=100, default="")
    mcc_or_nonstan = models.CharField(max_length=100,  blank=False)
    board_desc = models.CharField(max_length=100)
    board_qty = models.IntegerField(blank=False, null=True)
    mcc_description = models.CharField(max_length=100, blank=True)
    hori_bus_bar_desc = models.CharField(max_length=100, blank=True, help_text='Amps')
    control_bus_bar_qty = models.IntegerField(default=0)
    front_access_panel = models.BooleanField(default=True)
    no_of_bus_section = models.IntegerField(default=0)
    delete = models.BooleanField(default=False)
    phase = models.CharField(choices=[('D', 'D'), ('T', 'T'), ('N', 'N')], default="", max_length=10,
                             help_text='D=DP/T=TP/N=TPN')

    def __str__(self):
        return  "Board Id : " +str(self.id) + ", " "Board Code : " +self.board_code + ", " + " Description : " +self.board_desc


class ModuleDetails(models.Model):
    # id = models.IntegerField(primary_key=True)
    board_detail = models.ForeignKey(BoardDetails, on_delete=models.CASCADE, null=True, blank=True)
    tender_id = models.CharField(max_length=20)
    tender_version = models.CharField(max_length=20)
    board_id = models.CharField(max_length=30)
    module_id = models.CharField(max_length=30)
    module_code = models.CharField(max_length=30, default="")
    module_type = models.CharField(max_length=30)
    description = models.TextField(max_length=60)
    quantity = models.IntegerField(default=0)
    quantity2 = models.IntegerField(default=0)
    quantity3 = models.IntegerField(default=0, blank=True)
    quantity4 = models.IntegerField(default=0, blank=True)
    quantity5 = models.IntegerField(default=0,  blank=True)
    total_quantity = models.FloatField(default=0)
    type = models.CharField(choices=[('incoming', 'Incoming'), ('bus_coupler', 'Bus Coupler'), ('outgoing', 'Outgoing')],
                            default="", max_length=20,)
    bus_section = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                   default="", max_length=10)
    revision = models.CharField(max_length=50, default="")

    def __str__(self):
        return "Module Id : " + self.module_id + " / " + " Description : " + self.description


class ComponentDetails(models.Model):
    module_detail = models.ForeignKey(ModuleDetails, on_delete=models.CASCADE, null=True, blank=True)
    # id = models.IntegerField(primary_key=True)
    tender_code = models.CharField(max_length=20)
    tender_version = models.CharField(max_length=20)
    module_id = models.CharField(max_length=30)
    component_id = models.CharField(max_length=30)
    description = models.TextField(max_length=60)
    quantity = models.IntegerField(default=0)


class BoardsAll(models.Model):
    # id = models.IntegerField()
    description = models.TextField(max_length=60)


class ModuleAll(models.Model):
    # id = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=60)


class ComponentsAll(models.Model):
    # id = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=60)


class ModulesMix(models.Model):
    # id = models.IntegerField(primary_key=True)
    module_type = models.CharField(max_length=60)
    module_id = models.IntegerField()
    component_id = models.CharField(max_length=30)
    component_quantity = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()


class Distributor(models.Model):
    name = models.CharField(max_length=100)
    products= models.ManyToManyField(Product)


class TenderDataProcess(Process):
    # tender_details = models.ForeignKey(TenderDataDetails, on_delete=models.CASCADE, default=False)
    # board_detail = models.ForeignKey(BoardDetails, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", default=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    # last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_updated_by", default=True)
    active = models.BooleanField(default=False)




