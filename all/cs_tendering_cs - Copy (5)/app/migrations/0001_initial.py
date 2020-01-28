# Generated by Django 2.2.7 on 2019-12-24 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewflow', '0006_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.CharField(max_length=20, null=True)),
                ('board_code', models.CharField(blank=True, max_length=100, null=True)),
                ('stand_or_non', models.CharField(choices=[('standard', 'STANDARD'), ('nonstandard', 'NONSTANDARD')], default='', max_length=100)),
                ('indoor_or_outdoor', models.CharField(choices=[('indoor', 'INDOOR'), ('outdoor', 'OUTDOOOR')], default='', max_length=100)),
                ('mcc_or_nonstan', models.CharField(max_length=100)),
                ('board_desc', models.CharField(default='', max_length=100)),
                ('board_qty', models.IntegerField(null=True)),
                ('mcc_description', models.CharField(blank=True, max_length=100)),
                ('hori_bus_bar_desc', models.CharField(blank=True, help_text='Amps', max_length=100)),
                ('control_bus_bar_qty', models.IntegerField(default=0)),
                ('front_access_panel', models.BooleanField(default=True)),
                ('delete', models.BooleanField(default=False)),
                ('phase', models.CharField(choices=[('D', 'D'), ('T', 'T'), ('N', 'N')], default='', help_text='D=DP/T=TP/N=TPN', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='BOARDS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BRD_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('BRD_DESC', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY', models.CharField(blank=True, max_length=50, null=True)),
                ('BRD_STN', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_MCC', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_VBCC', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_PCC', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_PDUM', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_PRL8', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_PRL4', models.CharField(blank=True, max_length=50, null=True)),
                ('BQTY_DUM', models.CharField(blank=True, max_length=50, null=True)),
                ('BCMP_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BDOT_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BCGL_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BPGL_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BPFB_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BMFB_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BLFB_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BWRG_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BLWRG_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BBB_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BCBB_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BSPC_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('BUNP', models.CharField(blank=True, max_length=50, null=True)),
                ('BFRG', models.CharField(blank=True, max_length=50, null=True)),
                ('BMLPF', models.CharField(blank=True, max_length=50, null=True)),
                ('BERTC', models.CharField(blank=True, max_length=50, null=True)),
                ('BTOTAL', models.CharField(blank=True, max_length=50, null=True)),
                ('BHBB_RTNG', models.CharField(blank=True, max_length=50, null=True)),
                ('BRD_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_PHS', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('BCBB_QTY', models.CharField(blank=True, max_length=50, null=True)),
                ('FRO_ACCS', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BodyDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.CharField(max_length=20, null=True)),
                ('panel_sheet', models.CharField(choices=[('hrc', 'HRC'), ('crc', 'CRC')], max_length=3)),
                ('epoxy_paint', models.BooleanField(default=False)),
                ('shrouts', models.BooleanField(default=False)),
                ('htc_bolt', models.BooleanField(default=False)),
                ('shutter_mcc', models.BooleanField(default=False)),
                ('bus_bar', models.CharField(choices=[('alum.', 'Alum.'), ('copper', 'Copper')], max_length=7)),
                ('pvc_sleeves', models.BooleanField(default=False)),
                ('base_frame', models.BooleanField(default=False)),
                ('gland_comp', models.CharField(choices=[('single', 'Single'), ('double', 'Double')], max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='BUSBAR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BB_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('BB_PRIC', models.CharField(blank=True, max_length=50, null=True)),
                ('BB_OLD', models.CharField(blank=True, max_length=50, null=True)),
                ('BS_PRIC', models.CharField(blank=True, max_length=50, null=True)),
                ('BPVC_PRIC', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CLAS_DAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MODU_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('NO_OF_CLAS', models.IntegerField(blank=True, null=True)),
                ('CLASS1', models.IntegerField(blank=True, null=True)),
                ('CLASS2', models.IntegerField(blank=True, null=True)),
                ('CLASS3', models.IntegerField(blank=True, null=True)),
                ('CLASS4', models.IntegerField(blank=True, null=True)),
                ('CLASS5', models.IntegerField(blank=True, null=True)),
                ('CLASS6', models.IntegerField(blank=True, null=True)),
                ('CLASS7', models.IntegerField(blank=True, null=True)),
                ('CLASS8', models.IntegerField(blank=True, null=True)),
                ('CLASS9', models.IntegerField(blank=True, null=True)),
                ('CLASS10', models.IntegerField(blank=True, null=True)),
                ('CLASS11', models.IntegerField(blank=True, null=True)),
                ('CLASS12', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CNONSIZE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('WIDTH', models.FloatField(blank=True, null=True)),
                ('HEIGHT', models.FloatField(blank=True, null=True)),
                ('DEPTH', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='COMP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('COMP_CODE', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_CONM', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_NAME', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_RAT', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_CLAS', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_CLAS1', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_CLAS2', models.CharField(blank=True, max_length=100, null=True)),
                ('OLD_PRIC', models.CharField(blank=True, max_length=100, null=True)),
                ('NEW_PRIC', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_PRIC', models.CharField(blank=True, max_length=100, null=True)),
                ('CURR_JUN06', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_DESC', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_PRNT', models.CharField(blank=True, max_length=100, null=True)),
                ('JUN06', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='COMPCO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('COMP_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_CONM', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_NAME', models.CharField(blank=True, max_length=50, null=True)),
                ('DISC', models.CharField(blank=True, max_length=50, null=True)),
                ('EXCS', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='COMPDIS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('COMP_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_CONM', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_NAME', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_DESC', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_PRIC', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_DIS', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='COMPMAST',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MODU_NAME', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_NAME', models.CharField(blank=True, max_length=50, null=True)),
                ('QTY', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DOTMOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DMOD_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('DOTDESC', models.CharField(blank=True, max_length=50, null=True)),
                ('DOTCST', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GLAND',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GLAND_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('GLAND_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('GLAND_DESC', models.CharField(blank=True, max_length=50, null=True)),
                ('GLAND_RATE', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LUG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LUG_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('LUG_RATE', models.CharField(blank=True, max_length=50, null=True)),
                ('LUG_DESC', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LUGLNDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GLAND_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('NO_CORES', models.FloatField(blank=True, null=True)),
                ('LUG_CODE', models.FloatField(blank=True, null=True)),
                ('GLAND_CODE', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MAKE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NAME', models.CharField(blank=True, max_length=100, null=True)),
                ('COMP_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('NO_OPTIONS', models.FloatField(blank=True, null=True)),
                ('NO_OF_CHAR', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MODCOMP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CMOD_CD', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('COMP_QTY', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MODU_RTG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCH_MCODE', models.CharField(blank=True, max_length=50, null=True)),
                ('MOD_RTG', models.CharField(blank=True, max_length=50, null=True)),
                ('MOD_RTGCO', models.CharField(blank=True, max_length=50, null=True)),
                ('UNITS', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MODU_SIZ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CMOD_CD', models.CharField(blank=True, max_length=50, null=True)),
                ('SIZE_FIX', models.CharField(blank=True, max_length=50, null=True)),
                ('SIZE_DT', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MODUNAME',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MOD_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('MOD_NAME', models.CharField(blank=True, max_length=50, null=True)),
                ('FCH_MCODE', models.CharField(blank=True, max_length=50, null=True)),
                ('TOT_RTGS', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='P',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PN_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_DESC', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_DPTH', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_HT', models.CharField(blank=True, max_length=50, null=True)),
                ('PPCK_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('PHRC_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('PCRC_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('PBF_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('PEPX_CST', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_SHUT', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_SHRD', models.CharField(blank=True, max_length=50, null=True)),
                ('LABOUR', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RATDES',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FCH_MCODE', models.CharField(blank=True, max_length=50, null=True)),
                ('CLASS', models.IntegerField(blank=True, null=True)),
                ('DESRIP', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ROWPO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('POS_NO', models.IntegerField(blank=True, null=True)),
                ('SCRE_P', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SEQUENCE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NBS', models.IntegerField(blank=True, null=True)),
                ('NBC', models.IntegerField(blank=True, null=True)),
                ('FBC_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('SBC_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('NIC', models.IntegerField(blank=True, null=True)),
                ('IC_TYPEM', models.CharField(blank=True, max_length=50, null=True)),
                ('IC_TYPEP', models.CharField(blank=True, max_length=50, null=True)),
                ('SEQUENCE', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TEM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ORDER_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('CUSTOMER', models.CharField(blank=True, max_length=100, null=True)),
                ('PROJECT', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_SHET', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_BF', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_EPNT', models.CharField(blank=True, max_length=50, null=True)),
                ('PN_GLCMP', models.CharField(blank=True, max_length=50, null=True)),
                ('BB_TYPE', models.CharField(blank=True, max_length=50, null=True)),
                ('PVC_SLEV', models.CharField(blank=True, max_length=50, null=True)),
                ('PROC_FLAG', models.CharField(blank=True, max_length=50, null=True)),
                ('HTS_BOLT', models.CharField(blank=True, max_length=50, null=True)),
                ('SHRO_UDS', models.CharField(blank=True, max_length=50, null=True)),
                ('NA_USER', models.CharField(blank=True, max_length=50, null=True)),
                ('COMNO', models.CharField(blank=True, max_length=50, null=True)),
                ('ORUSE_FLAG', models.CharField(blank=True, max_length=50, null=True)),
                ('CHK_DIR', models.CharField(blank=True, max_length=50, null=True)),
                ('BACK_UP_FL', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TenderDataProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='WMOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WMOD_CODE', models.CharField(blank=True, max_length=50, null=True)),
                ('WDESC', models.CharField(blank=True, max_length=50, null=True)),
                ('WBCST', models.FloatField(blank=True, null=True)),
                ('WCCST', models.FloatField(blank=True, null=True)),
                ('WLABOUR', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TenderDataDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_code', models.CharField(max_length=20)),
                ('tender_version', models.CharField(max_length=20)),
                ('customer_name', models.CharField(max_length=250)),
                ('project_name', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.CharField(max_length=20)),
                ('tender_version', models.CharField(blank=True, max_length=20)),
                ('board_id', models.CharField(blank=True, max_length=30)),
                ('module_id', models.CharField(blank=True, max_length=30)),
                ('module_code', models.CharField(blank=True, default='', max_length=30)),
                ('module_type', models.CharField(blank=True, max_length=30)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
                ('quantity', models.IntegerField(blank=True, default=0)),
                ('quantity2', models.IntegerField(blank=True, default=0)),
                ('quantity3', models.IntegerField(blank=True, default=0)),
                ('quantity4', models.IntegerField(blank=True, default=0)),
                ('quantity5', models.IntegerField(blank=True, default=0)),
                ('total_quantity', models.FloatField(blank=True, default=0)),
                ('type', models.CharField(blank=True, choices=[('incoming', 'Incoming'), ('bus_coupler', 'Bus Coupler'), ('outgoing', 'Outgoing')], default='', max_length=20)),
                ('bus_section', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='', max_length=10)),
                ('revision', models.CharField(blank=True, default='', max_length=50)),
                ('board_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.BoardDetails')),
            ],
        ),
        migrations.CreateModel(
            name='ComponentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_id', models.CharField(max_length=20)),
                ('tender_version', models.CharField(max_length=20)),
                ('module_id', models.CharField(blank=True, max_length=30)),
                ('component_id', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=60)),
                ('quantity', models.IntegerField(default=0)),
                ('board_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.BoardDetails')),
                ('module_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ModuleDetails')),
            ],
        ),
    ]
