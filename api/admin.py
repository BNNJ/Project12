from django.contrib import admin

from .models import Customer, Contract, ContractStatus, Event, EventStatus

admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(ContractStatus)
admin.site.register(Event)
admin.site.register(EventStatus)
