from django.contrib import admin

from representatives.models import Email, WebSite, Address, Phone, Country, Constituency
from legislature.models import MMandate, MRepresentative, MGroup


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class WebsiteInline(admin.TabularInline):
    model = WebSite
    extra = 0


class AdressInline(admin.StackedInline):
    model = Address
    extra = 0


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'birth_place')
    search_fields = ('first_name', 'last_name', 'birth_place')
    list_filter = ('gender', )
    inlines = [
        PhoneInline,
        EmailInline,
        WebsiteInline,
        AdressInline,
    ]


class MandateAdmin(admin.ModelAdmin):
    list_display = ('representative', 'group', 'role', 'constituency', 'begin_date', 'end_date', 'active')
    search_fields = ('representative', 'group', 'constituency')
    # list_filter = ('role',)


admin.site.register(MRepresentative, RepresentativeAdmin)

# admin.site.register(Country)

admin.site.register(MMandate, MandateAdmin)

admin.site.register(MGroup)
# admin.site.register(Constituency)
