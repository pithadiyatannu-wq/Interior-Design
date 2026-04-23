from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'phone', "role", "status","id_proof")
    search_fields = ('name', 'email')

@admin.register(Contact_detail)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'timestamp')

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'date_of_birth', 'profession','bio','user_image')

@admin.register(DesignerProfile)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'address', 'designerprofile_image', 'company_name', "company_address", "years_of_experience","specialization","rating","availability")

@admin.register(Bidding)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('designer', 'requirement', 'bid_amount','payment_date','payment_mode','razorpay_order_id','razorpay_payment_id', 'razorpay_signature', 'offline_reference','offline_remarks','address','status')

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Requirement)
class RequirementsAdmin(admin.ModelAdmin):
    list_display = ('user', 'req_name','initial_amount','req_desc', 'req_status','req_img','current_highest_bid','bid_end_date','minimum_bid_increment','creation_date')

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('id','designer', 'category','design_name', 'design_price','design_desc','pic1')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'designer', 'get_designs', 'total_price', 'payment_mode','razorpay_order_id', 'razorpay_payment_id','razorpay_signature', 'status', 'offline_reference','offline_remarks','address', 'created_at')

    def get_designs(self, obj):
        return obj.designs.count()
    get_designs.short_description = 'Design Count'

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user','design','ratings','comment','timestamp')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user','subject','description','timestamp')