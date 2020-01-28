from django.db import models
from viewflow.models import Process
from django.contrib.auth.models import User
import re
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chipped.settings.common")
# from django.contrib.admin import ModelAdmin, actions
from autoslug import AutoSlugField
from django.conf import settings


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


class BOARDS(models.Model):
    BRD_CODE = models.CharField(max_length=50, blank=True, null=True)
    BRD_DESC = models.CharField(max_length=50, blank=True, null=True)
    BQTY = models.CharField(max_length=50, blank=True, null=True)
    BRD_STN = models.CharField(max_length=50, blank=True, null=True)
    BQTY_MCC = models.CharField(max_length=50, blank=True, null=True)
    BQTY_VBCC = models.CharField(max_length=50, blank=True, null=True)
    BQTY_PCC = models.CharField(max_length=50, blank=True, null=True)
    BQTY_PDUM = models.CharField(max_length=50, blank=True, null=True)
    BQTY_PRL8 = models.CharField(max_length=50, blank=True, null=True)
    BQTY_PRL4 = models.CharField(max_length=50, blank=True, null=True)
    BQTY_DUM = models.CharField(max_length=50, blank=True, null=True)
    BCMP_CST = models.CharField(max_length=50, blank=True, null=True)
    BDOT_CST = models.CharField(max_length=50, blank=True, null=True)
    BCGL_CST = models.CharField(max_length=50, blank=True, null=True)
    BPGL_CST = models.CharField(max_length=50, blank=True, null=True)
    BPFB_CST = models.CharField(max_length=50, blank=True, null=True)
    BMFB_CST = models.CharField(max_length=50, blank=True, null=True)
    BLFB_CST = models.CharField(max_length=50, blank=True, null=True)
    BWRG_CST = models.CharField(max_length=50, blank=True, null=True)
    BLWRG_CST = models.CharField(max_length=50, blank=True, null=True)
    BBB_CST = models.CharField(max_length=50, blank=True, null=True)
    BCBB_CST = models.CharField(max_length=50, blank=True, null=True)
    BSPC_CST = models.CharField(max_length=50, blank=True, null=True)
    BUNP = models.CharField(max_length=50, blank=True, null=True)
    BFRG = models.CharField(max_length=50, blank=True, null=True)
    BMLPF = models.CharField(max_length=50, blank=True, null=True)
    BERTC = models.CharField(max_length=50, blank=True, null=True)
    BTOTAL = models.CharField(max_length=50, blank=True, null=True)
    BHBB_RTNG = models.CharField(max_length=50, blank=True, null=True)
    BRD_TYPE = models.CharField(max_length=50, blank=True, null=True)
    PN_PHS = models.CharField(max_length=50, blank=True, null=True)
    PN_CODE = models.CharField(max_length=50, blank=True, null=True)
    BCBB_QTY = models.CharField(max_length=50, blank=True, null=True)
    FRO_ACCS = models.CharField(max_length=50, blank=True, null=True)


class BUSBAR(models.Model):
    BB_CODE = models.CharField(max_length=50, blank=True, null=True)
    BB_PRIC = models.CharField(max_length=50, blank=True, null=True)
    BB_OLD = models.CharField(max_length=50, blank=True, null=True)
    BS_PRIC = models.CharField(max_length=50, blank=True, null=True)
    BPVC_PRIC = models.CharField(max_length=50, blank=True, null=True)


class COMPCO(models.Model):
    COMP_CODE = models.CharField(max_length=50, blank=True, null=True)
    COMP_CONM = models.CharField(max_length=50, blank=True, null=True)
    COMP_NAME = models.CharField(max_length=50, blank=True, null=True)
    DISC = models.CharField(max_length=50, blank=True, null=True)
    EXCS = models.CharField(max_length=50, blank=True, null=True)


class COMPDIS(models.Model):
    COMP_CODE = models.CharField(max_length=50, blank=True, null=True)
    COMP_CONM = models.CharField(max_length=50, blank=True, null=True)
    COMP_NAME = models.CharField(max_length=50, blank=True, null=True)
    COMP_DESC = models.CharField(max_length=50, blank=True, null=True)
    COMP_PRIC = models.CharField(max_length=50, blank=True, null=True)
    COMP_DIS = models.CharField(max_length=50, blank=True, null=True)


class COMPMAST(models.Model):
    MODU_NAME = models.CharField(max_length=50, blank=True, null=True)
    COMP_NAME = models.CharField(max_length=50, blank=True, null=True)
    QTY = models.FloatField(blank=True, null=True)


class DOTMOD(models.Model):
    DMOD_CODE = models.CharField(max_length=50, blank=True, null=True)
    DOTDESC = models.CharField(max_length=50, blank=True, null=True)
    DOTCST = models.CharField(max_length=50, blank=True, null=True)


class LUG(models.Model):
    LUG_CODE = models.CharField(max_length=50, blank=True, null=True)
    LUG_RATE = models.CharField(max_length=50, blank=True, null=True)
    LUG_DESC = models.CharField(max_length=50, blank=True, null=True)


class LUGLNDC(models.Model):
    GLAND_TYPE = models.CharField(max_length=50, blank=True, null=True)
    NO_CORES = models.FloatField(blank=True, null=True)
    LUG_CODE = models.FloatField(blank=True, null=True)
    GLAND_CODE = models.FloatField(blank=True, null=True)


class GLAND(models.Model):
    GLAND_TYPE = models.CharField(max_length=50, blank=True, null=True)
    GLAND_CODE = models.CharField(max_length=50, blank=True, null=True)
    GLAND_DESC = models.CharField(max_length=50, blank=True, null=True)
    GLAND_RATE = models.CharField(max_length=50, blank=True, null=True)


class CLAS_DAT(models.Model):
    MODU_CODE = models.CharField(max_length=50, blank=True, null=True)
    NO_OF_CLAS = models.IntegerField(blank=True, null=True)
    CLASS1 = models.IntegerField(blank=True, null=True)
    CLASS2 = models.IntegerField(blank=True, null=True)
    CLASS3 = models.IntegerField(blank=True, null=True)
    CLASS4 = models.IntegerField(blank=True, null=True)
    CLASS5 = models.IntegerField(blank=True, null=True)
    CLASS6 = models.IntegerField(blank=True, null=True)
    CLASS7 = models.IntegerField(blank=True, null=True)
    CLASS8 = models.IntegerField(blank=True, null=True)
    CLASS9 = models.IntegerField(blank=True, null=True)
    CLASS10 = models.IntegerField(blank=True, null=True)
    CLASS11 = models.IntegerField(blank=True, null=True)
    CLASS12 = models.IntegerField(blank=True, null=True)


class CNONSIZE(models.Model):
    TYPE = models.CharField(max_length=50, blank=True, null=True)
    WIDTH = models.FloatField(blank=True, null=True)
    HEIGHT = models.FloatField(blank=True, null=True)
    DEPTH = models.FloatField(blank=True, null=True)


class COMP(models.Model):
    COMP_CODE = models.CharField(max_length=100, blank=True, null=True)
    COMP_CONM = models.CharField(max_length=100, blank=True, null=True)
    COMP_NAME = models.CharField(max_length=100, blank=True, null=True)
    COMP_RAT = models.CharField(max_length=100, blank=True, null=True)
    COMP_CLAS = models.CharField(max_length=100, blank=True, null=True)
    COMP_CLAS1 = models.CharField(max_length=100, blank=True, null=True)
    COMP_CLAS2 = models.CharField(max_length=100, blank=True, null=True)
    OLD_PRIC = models.CharField(max_length=100, blank=True, null=True)
    NEW_PRIC = models.CharField(max_length=100, blank=True, null=True)
    COMP_PRIC = models.CharField(max_length=100, blank=True, null=True)
    CURR_JUN06 = models.CharField(max_length=100, blank=True, null=True)
    COMP_DESC = models.CharField(max_length=100, blank=True, null=True)
    COMP_PRNT = models.CharField(max_length=100, blank=True, null=True)
    JUN06 = models.CharField(max_length=100, blank=True, null=True)


class MAKE(models.Model):
    NAME = models.CharField(max_length=100, blank=True, null=True)
    COMP_CODE = models.CharField(max_length=50, blank=True, null=True)
    NO_OPTIONS = models.FloatField(blank=True, null=True)
    NO_OF_CHAR = models.FloatField( blank=True, null=True)


class MODCOMP(models.Model):
    CMOD_CD = models.CharField(max_length=50, blank=True, null=True)
    COMP_CODE = models.CharField(max_length=50, blank=True, null=True)
    COMP_QTY = models.IntegerField(blank=True, null=True)


class MODU_RTG(models.Model):
    FCH_MCODE = models.CharField(max_length=50, blank=True, null=True)
    MOD_RTG = models.CharField(max_length=50, blank=True, null=True)
    MOD_RTGCO = models.CharField(max_length=50, blank=True, null=True)
    UNITS = models.CharField(max_length=50, blank=True, null=True)


class MODU_SIZ(models.Model):
    CMOD_CD = models.CharField(max_length=50, blank=True, null=True)
    SIZE_FIX = models.CharField(max_length=50, blank=True, null=True)
    SIZE_DT = models.CharField(max_length=50, blank=True, null=True)


class MODUNAME(models.Model):
    MOD_TYPE = models.CharField(max_length=50, blank=True, null=True)
    MOD_NAME = models.CharField(max_length=50, blank=True, null=True)
    FCH_MCODE = models.CharField(max_length=50, blank=True, null=True)
    TOT_RTGS = models.CharField(max_length=50, blank=True, null=True)


class P(models.Model):
    PN_CODE = models.CharField(max_length=50, blank=True, null=True)
    PN_DESC = models.CharField(max_length=50, blank=True, null=True)
    PN_DPTH = models.CharField(max_length=50, blank=True, null=True)
    PN_HT = models.CharField(max_length=50, blank=True, null=True)
    PPCK_CST = models.CharField(max_length=50, blank=True, null=True)
    PHRC_CST = models.CharField(max_length=50, blank=True, null=True)
    PCRC_CST = models.CharField(max_length=50, blank=True, null=True)
    PBF_CST = models.CharField(max_length=50, blank=True, null=True)
    PEPX_CST = models.CharField(max_length=50, blank=True, null=True)
    PN_SHUT = models.CharField(max_length=50, blank=True, null=True)
    PN_SHRD = models.CharField(max_length=50, blank=True, null=True)
    LABOUR = models.CharField(max_length=50, blank=True, null=True)


class RATDES(models.Model):
    FCH_MCODE = models.CharField(max_length=50, blank=True, null=True)
    CLASS = models.IntegerField(blank=True, null=True)
    DESRIP = models.CharField(max_length=50, blank=True, null=True)


class ROWPO(models.Model):
    POS_NO = models.IntegerField(blank=True, null=True)
    SCRE_P = models.IntegerField(blank=True, null=True)


class SEQUENCE(models.Model):
    NBS = models.IntegerField(blank=True, null=True)
    NBC = models.IntegerField(blank=True, null=True)
    FBC_TYPE = models.CharField(max_length=50, blank=True, null=True)
    SBC_TYPE = models.CharField(max_length=50, blank=True, null=True)
    NIC = models.IntegerField(blank=True, null=True)
    IC_TYPEM = models.CharField(max_length=50, blank=True, null=True)
    IC_TYPEP = models.CharField(max_length=50, blank=True, null=True)
    SEQUENCE = models.CharField(max_length=50, blank=True, null=True)


class TEM(models.Model):
    ORDER_CODE = models.CharField(max_length=50, blank=True, null=True)
    CUSTOMER = models.CharField(max_length=100, blank=True, null=True)
    PROJECT = models.CharField(max_length=50, blank=True, null=True)
    PN_SHET = models.CharField(max_length=50, blank=True, null=True)
    PN_BF = models.CharField(max_length=50, blank=True, null=True)
    PN_EPNT = models.CharField(max_length=50, blank=True, null=True)
    PN_GLCMP = models.CharField(max_length=50, blank=True, null=True)
    BB_TYPE = models.CharField(max_length=50, blank=True, null=True)
    PVC_SLEV = models.CharField(max_length=50, blank=True, null=True)
    PROC_FLAG = models.CharField(max_length=50, blank=True, null=True)
    HTS_BOLT = models.CharField(max_length=50, blank=True, null=True)
    SHRO_UDS = models.CharField(max_length=50, blank=True, null=True)
    NA_USER = models.CharField(max_length=50, blank=True, null=True)
    COMNO = models.CharField(max_length=50, blank=True, null=True)
    ORUSE_FLAG = models.CharField(max_length=50, blank=True, null=True)
    CHK_DIR = models.CharField(max_length=50, blank=True, null=True)
    BACK_UP_FL = models.CharField(max_length=50, blank=True, null=True)


class WMOD(models.Model):
    WMOD_CODE = models.CharField(max_length=50, blank=True, null=True)
    WDESC = models.CharField(max_length=50, blank=True, null=True)
    WBCST = models.FloatField(blank=True, null=True)
    WCCST = models.FloatField(blank=True, null=True)
    WLABOUR = models.FloatField(blank=True, null=True)


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
    tender_id = models.CharField(max_length=20, null=True, blank=False)
    # tender_version = models.CharField(max_length=20)
    # board_code = models.ForeignKey(
    #     'self',
    #     on_delete=models.CASCADE,
    #
    #     blank=True,
    #     related_name='related_board_models'
    # )
    board_code = models.CharField(max_length=100,   null=True, blank=True)
    stand_or_non = models.CharField(choices=[('standard', 'STANDARD'), ('nonstandard', 'NONSTANDARD')],
                                    max_length=100, default="")
    indoor_or_outdoor = models.CharField(choices=[('indoor', 'INDOOR'), ('outdoor', 'OUTDOOOR')],
                                         max_length=100, default="")
    mcc_or_nonstan = models.CharField(max_length=100,  blank=False)
    board_desc = models.CharField(max_length=100,  default='')
    # board_desc = models.ForeignKey(BoardsTableData, on_delete=models.CASCADE,  blank=True, null=True)
    board_qty = models.IntegerField(blank=False, null=True)
    mcc_description = models.CharField(max_length=100, blank=True)
    hori_bus_bar_desc = models.CharField(max_length=100, blank=True, help_text='Amps')
    control_bus_bar_qty = models.IntegerField(default=0)
    front_access_panel = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    phase = models.CharField(choices=[('D', 'D'), ('T', 'T'), ('N', 'N')], default="", max_length=10,
                             help_text='D=DP/T=TP/N=TPN')

    def __str__(self):
        # return "Board Code : " + self.board_code + ", " + " Description : " + self.board_desc
        return self.tender_id

    # def save(self, *args, **kwargs):
    #     board_code = self.board_code
    #     board_desc = self.board_desc
    #     print(board_desc,'44444444444444')
    #     super(BoardDetails, self).save(*args, **kwargs)


from django.db import IntegrityError
class ModuleDetails(models.Model):
    # id = models.IntegerField(primary_key=True)
    board_code = models.ForeignKey(BoardDetails, on_delete=models.CASCADE, null=True, blank=True)
    tender_id = models.CharField(max_length=20, default="")
    tender_version = models.CharField(max_length=20,blank=True)
    board_id = models.CharField(max_length=30,blank=True)
    module_id = models.CharField(max_length=30,blank=True)
    module_code = models.CharField(max_length=30, default="",blank=True)
    module_type = models.CharField(max_length=30,blank=True)
    description = models.CharField(max_length=200, blank=True, default="")
    quantity = models.IntegerField(default=0, blank=True)
    quantity2 = models.IntegerField(default=0,blank=True)
    quantity3 = models.IntegerField(default=0, blank=True)
    quantity4 = models.IntegerField(default=0, blank=True)
    quantity5 = models.IntegerField(default=0,  blank=True)
    total_quantity = models.FloatField(default=0,blank=True)
    type = models.CharField(choices=[('incoming', 'Incoming'), ('bus_coupler', 'Bus Coupler'), ('outgoing', 'Outgoing')],
                            default="", max_length=20, blank=True)
    bus_section = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                                   default="", max_length=10, blank=True)
    revision = models.CharField(max_length=50, default="", blank=True)

    # def __unicode__(self):
    #     return self.board_detail

    def __str__(self):
        return str(self.board_detail)
        # return self.description

    # def save(self, *args, **kwargs):
    #     if ModuleDetails.objects.filter(
    #         tender_id=self.tender_id,
    #     ).exists():
    #         raise IntegrityError
    #     super(ModuleDetails, self).save(*args, **kwargs)


class ComponentDetails(models.Model):
    board_detail = models.ForeignKey(BoardDetails, on_delete=models.CASCADE, null=True, blank=True)
    module_detail = models.ForeignKey(ModuleDetails, on_delete=models.CASCADE, null=True, blank=True)
    # board_detail = models.CharField(max_length=200, null=True, blank=False)
    # id = models.IntegerField(primary_key=True)
    tender_id = models.CharField(max_length=20)
    # tender_version = models.CharField(max_length=20, default="")
    module_id = models.CharField(max_length=30, blank=True)
    component_id = models.CharField(max_length=30)
    description = models.TextField(max_length=60)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.board_detail)

    # class Meta:
        # order_with_respect_to = 'brd_desc'


class TenderDataProcess(Process):
    # tender_details = models.ForeignKey(TenderDataDetails, on_delete=models.CASCADE, default=False)
    # board_detail = models.ForeignKey(BoardDetails, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by", default=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    # last_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_updated_by", default=True)
    active = models.BooleanField(default=False)




