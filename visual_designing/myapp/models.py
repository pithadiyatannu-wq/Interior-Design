from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Use this for month-based delta
# Create your models here.

class Login(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default="admin@123")
    phone = models.CharField(max_length=20, null=True, blank=True)

    ROLE = (
        ("Designer", "Designer"),
        ("User", "User"),
    )
    role = models.CharField(max_length=10, choices=ROLE, default='User')

    STATUS = (
        ("0", "unapproved"),
        ("1", "approved")
    )
    status = models.CharField(max_length=10, choices=STATUS, default='0')

    id_proof = models.FileField(upload_to='id_proofs/', null=True, blank=True, default=None)

    def pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.id_proof.url))
    pic.allow_tags = True

    def __str__(self):
        return self.name

class Contact_detail(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=30)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    address = models.TextField()
    date_of_birth = models.DateField(blank=True, null=True)
    profession = models.CharField(max_length=100)  # User's profession
    bio = models.TextField(blank=True, null=True)  # Brief introduction
    userprofile_image = models.ImageField(upload_to='media/', blank=True, null=True)

    def user_image(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.userprofile_image.url))
    user_image.allow_tags = True

    def __str__(self):
        return self.user.name

class DesignerProfile(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    designerprofile_image = models.ImageField(upload_to='seller_profiles/', blank=True, null=True)
    company_name  = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    years_of_experience = models.FloatField(blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(default=0.0)  # Changed to FloatField
    availability = models.CharField(max_length=40, choices=[('Available', 'Available'), ('Not Available', 'Not Available')], default='Available')

    def designer_image(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.designerprofile_image.url))
    designer_image.allow_tags = True

    def __str__(self):
        return f"{self.user.name}'s Designer Profile"

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Requirement(models.Model):
    REQUIREMENT_STATUS_CHOICES = [
        (0, 'Open'),
        (1, 'Close'),
    ]
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    req_name = models.CharField(max_length=150, null=False)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    req_desc = models.CharField(max_length=150, null=False)
    req_status = models.IntegerField(choices=REQUIREMENT_STATUS_CHOICES, null=False)
    req_img = models.ImageField(upload_to='products/', null=True, blank=True)
    current_highest_bid = models.IntegerField(default=0)
    bid_end_date = models.DateTimeField(null=True, blank=True)
    minimum_bid_increment = models.IntegerField(default=1)
    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)
    def req_pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.req_img.url))

    req_pic.allow_tags = True

    def __str__(self):
        return self.req_name

class Design(models.Model):
    designer = models.ForeignKey('Login', on_delete=models.CASCADE, limit_choices_to={'role': 'Designer'}, default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    design_name = models.CharField(max_length=250, null=False)
    design_price = models.IntegerField(null=False)
    design_desc = models.CharField(max_length=250, null=False)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def pic1(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.image.url))
    pic1.allow_tags = True

    def __str__(self):
        return self.design_name


class Booking(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('online', 'Online Payment'),
        ('offline', 'Offline Payment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('paid', 'Paid'),
        ('not paid', 'Not Paid'),
    ]
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    designer = models.ForeignKey(DesignerProfile, on_delete=models.CASCADE)
    designs = models.ManyToManyField(Design, blank=True, help_text="select any Design.")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)  # Payment mode
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    offline_reference = models.CharField(max_length=255, blank=True, null=True)  # Reference number for offline payment
    offline_remarks = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    address = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    created_at = models.DateTimeField(auto_now_add=True)

class Bidding(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('online', 'Online Payment'),
        ('offline', 'Offline Payment'),
    ]
    designer = models.ForeignKey(Login, on_delete=models.CASCADE)  # The user placing the bid
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)  # The product being bid on
    bid_amount = models.IntegerField()  # The amount the user is bidding
    payment_date = models.DateTimeField(auto_now=True)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)  # Payment mode
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    offline_reference = models.CharField(max_length=255, blank=True, null=True)  # Reference number for offline payment
    offline_remarks = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    address = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('paid', 'paid'),
        ('not paid', 'not paid'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status of the bid

    def __str__(self):
        return f"Bid by {self.designer.name} on {self.requirement.req_name} for {self.bid_amount}"

class Feedback(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE, default="")
    design = models.ForeignKey('Design', on_delete=models.CASCADE, null=True, blank=True, default='')
    ratings = models.IntegerField()
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.user.name} for design{self.design.design_name}"

class Complaint(models.Model):
    user = models.ForeignKey('Login', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Complaint from {self.user.name} - {self.subject}"