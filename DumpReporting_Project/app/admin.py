from django.contrib import admin
from .models import DUMPReport, MRNReportGSTNew,ContributionReport,CustomerLedgerPassbook,UserForm

admin.site.register(DUMPReport)
admin.site.register(MRNReportGSTNew)
admin.site.register(ContributionReport)
admin.site.register(UserForm)
admin.site.register(CustomerLedgerPassbook)
