# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppBoarddetails(models.Model):
    board_code = models.CharField(max_length=100)
    stand_or_non = models.CharField(max_length=100)
    indoor_or_outdoor = models.CharField(max_length=100)
    mcc_or_nonstan = models.CharField(max_length=100)
    board_desc = models.CharField(max_length=100)
    board_qty = models.IntegerField(blank=True, null=True)
    mcc_description = models.CharField(max_length=100)
    hori_bus_bar_desc = models.CharField(max_length=100)
    control_bus_bar_qty = models.IntegerField()
    front_access_panel = models.BooleanField()
    phase = models.CharField(max_length=10)
    delete = models.BooleanField()
    tender_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_boarddetails'


class AppBoardsAll(models.Model):
    brd_code = models.CharField(max_length=50, blank=True, null=True)
    brd_desc = models.CharField(max_length=50, blank=True, null=True)
    bqty = models.CharField(max_length=50, blank=True, null=True)
    brd_stn = models.CharField(max_length=50, blank=True, null=True)
    bqty_mcc = models.CharField(max_length=50, blank=True, null=True)
    bqty_vbcc = models.CharField(max_length=50, blank=True, null=True)
    bqty_pcc = models.CharField(max_length=50, blank=True, null=True)
    bqty_pdum = models.CharField(max_length=50, blank=True, null=True)
    bqty_prl8 = models.CharField(max_length=50, blank=True, null=True)
    bqty_prl4 = models.CharField(max_length=50, blank=True, null=True)
    bqty_dum = models.CharField(max_length=50, blank=True, null=True)
    bcmp_cst = models.CharField(max_length=50, blank=True, null=True)
    bdot_cst = models.CharField(max_length=50, blank=True, null=True)
    bcgl_cst = models.CharField(max_length=50, blank=True, null=True)
    bpgl_cst = models.CharField(max_length=50, blank=True, null=True)
    bpfb_cst = models.CharField(max_length=50, blank=True, null=True)
    bmfb_cst = models.CharField(max_length=50, blank=True, null=True)
    blfb_cst = models.CharField(max_length=50, blank=True, null=True)
    bwrg_cst = models.CharField(max_length=50, blank=True, null=True)
    blwrg_cst = models.CharField(max_length=50, blank=True, null=True)
    bbb_cst = models.CharField(max_length=50, blank=True, null=True)
    bcbb_cst = models.CharField(max_length=50, blank=True, null=True)
    bspc_cst = models.CharField(max_length=50, blank=True, null=True)
    bunp = models.CharField(max_length=50, blank=True, null=True)
    bfrg = models.CharField(max_length=50, blank=True, null=True)
    bmlpf = models.CharField(max_length=50, blank=True, null=True)
    bertc = models.CharField(max_length=50, blank=True, null=True)
    btotal = models.CharField(max_length=50, blank=True, null=True)
    bhbb_rtng = models.CharField(max_length=50, blank=True, null=True)
    brd_type = models.CharField(max_length=50, blank=True, null=True)
    pn_phs = models.CharField(max_length=50, blank=True, null=True)
    pn_code = models.CharField(max_length=50, blank=True, null=True)
    bcbb_qty = models.CharField(max_length=50, blank=True, null=True)
    fro_accs = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_boards_all'


class AppBoardsall(models.Model):
    bbb_cst = models.CharField(max_length=50)
    bcbb_cst = models.CharField(max_length=50)
    bcbb_qty = models.IntegerField()
    bcgl_cst = models.CharField(max_length=50)
    bcmp_cst = models.CharField(max_length=50)
    bdot_cst = models.CharField(max_length=50)
    bertc = models.CharField(max_length=50)
    bfrg = models.CharField(max_length=50)
    bhbb_rtng = models.CharField(max_length=50)
    blfb_cst = models.CharField(max_length=50)
    blwrg_cst = models.CharField(max_length=50)
    bmfb_cst = models.CharField(max_length=50)
    bmlpf = models.CharField(max_length=50)
    bpfb_cst = models.CharField(max_length=50)
    bpgl_cst = models.CharField(max_length=50)
    bqty = models.CharField(max_length=50)
    bqty_dum = models.CharField(max_length=50)
    bqty_mcc = models.CharField(max_length=50)
    bqty_pcc = models.CharField(max_length=50)
    bqty_pdum = models.CharField(max_length=50)
    bqty_prl4 = models.CharField(max_length=50)
    bqty_prl8 = models.CharField(max_length=50)
    bqty_vbcc = models.CharField(max_length=50)
    brd_code = models.CharField(max_length=50)
    brd_desc = models.CharField(max_length=50)
    brd_stn = models.CharField(max_length=50)
    brd_type = models.CharField(max_length=50)
    bspc_cst = models.CharField(max_length=50)
    btotal = models.CharField(max_length=50)
    bunp = models.CharField(max_length=50)
    bwrg_cst = models.CharField(max_length=50)
    frd_accs = models.CharField(max_length=50)
    pn_code = models.CharField(max_length=50)
    pn_phs = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'app_boardsall'


class AppBodydetails(models.Model):
    panel_sheet = models.CharField(max_length=3)
    epoxy_paint = models.BooleanField()
    shrouts = models.BooleanField()
    htc_bolt = models.BooleanField()
    shutter_mcc = models.BooleanField()
    bus_bar = models.CharField(max_length=7)
    pvc_sleeves = models.BooleanField()
    base_frame = models.BooleanField()
    gland_comp = models.CharField(max_length=7)
    tender_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_bodydetails'


class AppComponentdetails(models.Model):
    tender_id = models.CharField(max_length=20)
    tender_version = models.CharField(max_length=20)
    module_id = models.CharField(max_length=30)
    component_id = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    module_detail = models.ForeignKey('AppModuledetails', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_componentdetails'


class AppComponentsall(models.Model):
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'app_componentsall'


class AppDistributor(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'app_distributor'


class AppDistributorProducts(models.Model):
    distributor = models.ForeignKey(AppDistributor, models.DO_NOTHING)
    product = models.ForeignKey('AppProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_distributor_products'
        unique_together = (('distributor', 'product'),)


class AppModuleall(models.Model):
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'app_moduleall'


class AppModuledetails(models.Model):
    tender_id = models.CharField(max_length=20)
    tender_version = models.CharField(max_length=20)
    board_id = models.CharField(max_length=30)
    module_id = models.CharField(max_length=30)
    module_type = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    board_detail = models.ForeignKey(AppBoarddetails, models.DO_NOTHING, blank=True, null=True)
    bus_section = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=20)
    revision = models.CharField(max_length=50)
    module_code = models.CharField(max_length=30)
    quantity2 = models.IntegerField()
    quantity3 = models.IntegerField()
    quantity4 = models.IntegerField()
    quantity5 = models.IntegerField()
    total_quantity = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'app_moduledetails'


class AppModulesmix(models.Model):
    module_type = models.CharField(max_length=60)
    module_id = models.IntegerField()
    component_id = models.CharField(max_length=30)
    component_quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app_modulesmix'


class AppProduct(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app_product'


class AppTenderdatadetails(models.Model):
    tender_code = models.CharField(max_length=20)
    tender_version = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=250)
    project_name = models.CharField(max_length=250)
    active = models.BooleanField()
    created_by = models.ForeignKey('AuthUser', models.DO_NOTHING)
    last_updated_by = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'app_tenderdatadetails'


class AppTenderdataprocess(models.Model):
    process_ptr = models.ForeignKey('ViewflowProcess', models.DO_NOTHING, primary_key=True)
    created_date = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'app_tenderdataprocess'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FrontendModule(models.Model):
    label = models.CharField(max_length=50)
    installed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'frontend_module'


class ViewflowProcess(models.Model):
    flow_class = models.CharField(max_length=250)
    status = models.CharField(max_length=50)
    created = models.DateTimeField()
    finished = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viewflow_process'


class ViewflowTask(models.Model):
    flow_task = models.CharField(max_length=255)
    flow_task_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created = models.DateTimeField()
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=150)
    external_task_id = models.CharField(max_length=50, blank=True, null=True)
    owner_permission = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    process = models.ForeignKey(ViewflowProcess, models.DO_NOTHING)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viewflow_task'


class ViewflowTaskPrevious(models.Model):
    from_task = models.ForeignKey(ViewflowTask, models.DO_NOTHING)
    to_task = models.ForeignKey(ViewflowTask, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'viewflow_task_previous'
        unique_together = (('from_task', 'to_task'),)
