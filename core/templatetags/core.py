from django import template
from core.models import UserProfile



register = template.Library()
admin_tag = register.admin_tag if hasattr(register, 'admin_tag') else register.simple_tag

admin = UserProfile.objects.filter(is_superuser=True).first()

@admin_tag
def get_admin_contact(request):
    address = admin.address
    return address

@admin_tag
def get_admin_phone(request):
    phone = admin.phone
    return phone

@admin_tag
def get_admin_email(request):
    email = admin.email
    return email