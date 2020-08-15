from django.contrib import admin
from .models import Users, BankAccounts
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import UserChangeForm, UserCreationForm, AdminUserChangeForm, StaffUserCreationForm, StaffUserChangeForm
from simple_history.admin import SimpleHistoryAdmin
from simple_history.models import HistoricalRecords
from django.db.models import Sum, Q
import pdb

admin.site.site_header = 'GkBank'


class BankAccountsList(admin.StackedInline):
    model = BankAccounts
    extra = 1
    max_num = 1
    can_delete = False

class UsersAdmin(SimpleHistoryAdmin, BaseUserAdmin):
    """
        All customer that need to access their account
    """
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email','last_login','statements',)
    list_filter = ('username', 'email',)
    search_fields = ('username','email',)
    inlines = [BankAccountsList]

    def statements(self, obj):
    	return mark_safe('<button type="button" class="btn bg-purple btn-flat margin user_statements" data-id='"%s"'>%s</button>'%(obj.id, _('Enquiry')))

    def get_queryset(self, request):
        qs = super(UsersAdmin, self).get_queryset(request)
        if request.user.is_customer:
            return qs.filter(id=request.user.id)
        return qs.filter(is_superuser=True)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return super().get_form(request, obj, **kwargs)
        else:
            if request.user.is_customer:
                form = UserChangeForm
            else:
                form = AdminUserChangeForm
            return form

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'first_name', 'last_name',  'email', 'password', 'address', 'is_staff', 'is_active',)}
                     ),
                )
        if request.user.is_customer:
            return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'first_name', 'last_name',  'email', 'password', 'address', )}
                     ),
                )
        else:
            return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'first_name', 'last_name',  'email', 'password', 'address','is_staff', 'is_active', )}
                     ),
                )

    def has_add_permission(self, request):
        if request.user.is_customer:
            return False
        return super().has_add_permission(request)

admin.site.register(Users, UsersAdmin)


# Bank Staff user table
class StaffUser(Users):
    class Meta:
        verbose_name = _('Staff User')
        verbose_name_plural = _('   Staff Users')
    history = HistoricalRecords()

@admin.register(StaffUser)
class StaffUserAdmin(SimpleHistoryAdmin, BaseUserAdmin):
    """
        They are allowed to control or manage the bank resources
    """
    form = StaffUserChangeForm
    add_form = StaffUserCreationForm
    list_display = ('username', 'email','last_login',  'is_active', 'is_staff', 'is_superuser',)

    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name','email', 'password','is_staff', 'role', 'is_superuser', 'is_active', 'address',)}
         ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name',  'email', 'password','is_staff', 'role', 'is_superuser',  'is_active', 'address', )}
         ),
    )

    search_fields = ('username','email',)

    def get_queryset(self, request):
        qs = super(StaffUserAdmin, self).get_queryset(request)
        return qs.filter(is_superuser=True, is_staff=True)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False