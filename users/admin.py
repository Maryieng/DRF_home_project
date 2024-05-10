from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'city',)
    search_fields = ('email',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'well', 'lesson', 'method_pay', 'date_payment', 'money', 'link')
    search_fields = ('money', 'date_payment', 'method_pay',)
