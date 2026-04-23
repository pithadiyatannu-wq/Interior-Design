from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
# Create your views here.
def checksession(request):
    uid = request.session.get('log_id')

    if not uid:
        return None

    try:
        userdata = Login.objects.get(id=uid)
        is_designer = userdata.role == "Designer"

        if is_designer:
            try:
                profile = DesignerProfile.objects.get(user=userdata)
            except DesignerProfile.DoesNotExist:
                profile = None
        else:
            try:
                profile = UserProfile.objects.get(user=userdata)
            except UserProfile.DoesNotExist:
                profile = None

        context = {
            'userdata': userdata,
            'is_designer': is_designer,
            'profile': profile,
        }
        return context
    except Login.DoesNotExist:
        return None

def index(request):
    context = checksession(request)
    if context is None:
        context = {}
    alldesigners = DesignerProfile.objects.all()
    context['alldesigner'] = alldesigners
    return render(request,'index2.html',context)

def about(request):
    context = checksession(request)
    if context is None:
        context = {}
    alldesigners = DesignerProfile.objects.all()
    context['alldesigner'] = alldesigners
    return render(request,'about-us.html',context)

def contact(request):
    context = checksession(request)
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Subject = request.POST.get('subject')
        Message = request.POST.get('message')

        if Contact_detail.objects.filter(email=Email).exists():
            messages.error(request, 'You have already filled out contact details.')
            return redirect('contact')  # Assuming you have a URL pattern named 'contact1'
        else:
            contactdata = Contact_detail(name=Name, email=Email, subject=Subject, message=Message)
            contactdata.save()
            messages.success(request, 'Your contact details have been saved.')
            return redirect('index')  # Ensure 'index' is the name of your URL pattern or view function

    return render(request,'contact.html',context)

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name1')
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        phone = request.POST.get('phone1')
        role = request.POST.get('usertype')

        # Create a new Login object
        new_user = Login(name=name, email=email, password=password, phone=phone, role=role)

        # Check if id_proof1 exists in request.FILES
        if 'id_proof1' in request.FILES:
            id_proof = request.FILES['id_proof1']
            new_user.id_proof = id_proof

        # Save user based on their role
        if role == 'User':
            messages.info(request, 'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data inserted successfully. You can login now.')

        new_user.save()

        # Redirect to a success page
        return redirect('index')

    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        Email1 = request.POST['email2']
        Password1 = request.POST['password2']
        try:
            user = Login.objects.get(email=Email1, password=Password1)

        except Login.DoesNotExist:
            user = None

        if user is not None:
            if user.role == "User" and user.status == "0":
                print(user.role)
                print(user.status)
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_id'] = user.id
                request.session.save()
                messages.success(request, 'Login successful...')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email Id and Password. Please try again.')
            return redirect('/login')

    return render(request,'login.html')

def logout(request):
    try:
        del request.session['log_id']
        messages.success(request,'your logout successfully.')
    except:
        pass
    return render(request,'index2.html')

def adduserdetail(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address')
        Profile_image = request.FILES.get('profile_image')
        Dob = request.POST.get('date_of_birth')
        Profession = request.POST.get('profession')
        bio = request.POST.get('bio')

        userdata = UserProfile(user=Login(id=uid), address=Address,userprofile_image=Profile_image,date_of_birth=Dob, profession=Profession, bio=bio)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'adduser.html', context)

def showuser(request):
    context = checksession(request)
    uid = request.session['log_id']
    alluserdetails = UserProfile.objects.get(user=Login(id=uid))
    context.update({
        'alldetail': alluserdetails,
    })
    return render(request,'showuser.html', context)

def editprofile(request):
    context = checksession(request)
    uid = request.session['log_id']
    edituser = UserProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': edituser,
    })
    return render(request,'edituserdetail.html',context)

def update(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address1')
        Dob = request.POST.get('date_of_birth1')
        profession = request.POST.get('profession1')
        bio = request.POST.get('bio1')
        object = UserProfile.objects.get(user=uid)
        object.address=Address
        object.date_of_birth=Dob
        object.profession=profession
        object.bio=bio

        if 'profile_image1' in request.FILES:
            file = request.FILES['profile_image1']
            object.userprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showuser')
    return render(request,'edituserdetail.html',context)

def add_desingner(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address')
        Profile_image = request.FILES.get('designerprofile_image')
        Shopname = request.POST.get('company_name')
        Shopaddress = request.POST.get('company_address')
        yoe = request.POST.get('years_of_experience')
        spec = request.POST.get('specialization')
        ratings = request.POST.get('ratings')
        items = request.POST.get('items')
        Availibility = request.POST.get('availability')

        userdata = DesignerProfile(user=Login(id=uid), address=Address, designerprofile_image=Profile_image, company_name=Shopname, company_address=Shopaddress, years_of_experience=yoe, specialization=spec, rating=ratings,availability=Availibility)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'adddesigner.html', context)

def showdesigner(request):
    context = checksession(request)
    uid = request.session['log_id']
    allsellerdetails = DesignerProfile.objects.get(user=Login(id=uid))
    context.update({
        'sellerdetail': allsellerdetails,
    })
    return render(request,'showdesigner.html', context)

def edit_designer(request):
    context = checksession(request)
    uid = request.session['log_id']
    editsdesigner = DesignerProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': editsdesigner,
    })
    return render(request,'edit_designer.html',context)

def updatedesigner(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address2')
        shop = request.POST.get('company_name2')
        saddress = request.POST.get('company_address2')
        yearofexp = request.POST.get('years_of_experience2')
        speci = request.POST.get('specialization2')
        rat = request.POST.get('ratings2')
        avail = request.POST.get('availability2')
        object = DesignerProfile.objects.get(user=uid)
        object.address=Address
        object.company_name=shop
        object.company_address=saddress
        object.years_of_experience=yearofexp
        object.specialization=speci
        object.rating=rat
        object.availability=avail

        if 'seller1' in request.FILES:
            file = request.FILES['seller1']
            object.designerprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showdesigner')
    return render(request,'edit_designer.html',context)

def addrequirements(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('adduserdetail')
    uid = request.session['log_id']

    if request.method == 'POST':
        req_name = request.POST.get('req_name')
        req_desc = request.POST.get('req_desc')
        req_status = request.POST.get('req_status')
        design_image = request.FILES.get('design_image')

        product = Requirement(user=Login(id=uid), req_name=req_name, req_desc=req_desc, req_status=req_status, req_img=design_image)
        product.save()

        # Redirect or add additional logic as needed
        messages.success(request, 'Design added successfully')
        return redirect('index')

    return render(request,'upload_design_user.html', context)

def adddesign(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('add_desingner')
    uid = request.session['log_id']
    categories = Category.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        design_name = request.POST.get('design_name')
        design_price = request.POST.get('design_price')
        design_description = request.POST.get('design_desc')
        image = request.FILES.get('image')

        # Create or update Product instance
        category = Category.objects.get(id=category_id)

        product = Design(designer=Login(id=uid), category=category, design_name=design_name, design_price=design_price, design_desc=design_description,image=image)
        product.save()

        # Redirect or add additional logic as needed
        messages.success(request, 'Design added successfully')
        return redirect('index')

    context.update({'categories': categories})
    return render(request,'upload_design_designer.html', context)



def showrequirements(request):
    context = checksession(request)
    alldetail = Requirement.objects.all()
    context.update({'alldetail':alldetail})
    return render(request,'blog-2col.html',context)

def single_property(request, product_id):
    context = checksession(request)
    product = get_object_or_404(Requirement, id=product_id)
    is_sold = Bidding.objects.filter(requirement=product, status='paid').exists()  # Assuming 'paid' status indicates purchase

    context.update({'product': product, 'is_sold': is_sold})
    # Your logic here
    return render(request, 'requirementdetail.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

def place_bid(request, product_id):
    uid = request.session['log_id']
    product = get_object_or_404(Requirement, id=product_id)

    if request.method == "POST":
        bid_amount = int(request.POST.get('bid_amount'))

        # Handle None values
        current_highest_bid = product.current_highest_bid or 0
        initial_amount = product.initial_amount or 0

        if bid_amount > current_highest_bid and bid_amount > initial_amount:

            Bidding.objects.create(
                designer=Login.objects.get(id=uid),
                requirement=product,
                bid_amount=bid_amount,
                payment_date=timezone.now(),
                status='pending'
            )

            product.current_highest_bid = bid_amount
            product.save()

            messages.success(request, "Your bid has been placed successfully!")
            return redirect('/')

        else:
            messages.error(request, "Your bid must be higher than the current highest bid.")
            return redirect('/')

    return redirect('single_property', product_id=product.id)
def myrequirements(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('addowners')

    uid = request.session['log_id']  # Assuming you have user authentication
    products = Requirement.objects.filter(user=uid)

    context.update({"allproducts": products})
    return render(request,'myrequirements.html',context)

import razorpay
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

def manage_bids(request, product_id):

    context = checksession(request)
    uid = request.session['log_id']

    product = get_object_or_404(Requirement, id=product_id, user=Login(id=uid))
    bids = Bidding.objects.filter(requirement=product)

    if request.method == "POST":

        bid_id = request.POST.get("bid_id")
        bid = get_object_or_404(Bidding, id=bid_id)

        action = request.POST.get("action")

        # ---------------- REJECT BID ----------------
        if action == "reject":

            bid.status = "rejected"
            bid.save()

            messages.success(request, "Bid rejected successfully")
            return redirect(request.path)

        # ---------------- ACCEPT BID ----------------
        if action == "accept":
            bid.status = "accepted"
            bid.save()

            # Reject all other bids
            Bidding.objects.filter(requirement=product).exclude(id=bid.id).update(status="rejected")

            messages.success(request, "Bid accepted successfully. Other bids rejected.")

        # ---------------- ONLINE PAYMENT ----------------
        if action == "online_payment":

            client = razorpay.Client(
                auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f')
            )

            amount = int(bid.bid_amount * 100)

            data = {
                "amount": amount,
                "currency": "INR",
                "receipt": f"bid_{bid.id}",
                "payment_capture": 1
            }

            razorpay_order = client.order.create(data=data)

            bid.razorpay_order_id = razorpay_order['id']
            bid.payment_mode = "online"
            bid.save()

            context.update({
                "razorpay_payment": {
                    "amount": amount,
                    "order_id": razorpay_order['id'],
                    "key": "rzp_test_VQhEfe2NCXbbwI",
                },
                "bid": bid
            })

            return render(request, "manage_bids.html", context)

        # ---------------- OFFLINE PAYMENT ----------------
        if action == "offline_payment":

            offline_reference = request.POST.get("offline_reference")
            offline_remarks = request.POST.get("offline_remarks")
            address = request.POST.get("address")

            bid.offline_reference = offline_reference
            bid.offline_remarks = offline_remarks
            bid.address = address
            bid.payment_mode = "offline"
            bid.status = "paid"
            bid.save()

            messages.success(request, "Offline payment completed")
            return redirect(request.path)

    context.update({
        "bids": bids,
        "product": product
    })

    return render(request, "manage_bids.html", context)

def designer_bids(request):

    context = checksession(request)
    uid = request.session.get('log_id')

    user_bids = Bidding.objects.filter(designer=Login(id=uid))

    context.update({
        "user_bids": user_bids
    })

    return render(request, "designer_manage_bids.html", context)


def success(request):
    context = checksession(request)
    if not isinstance(context, dict):
        context = {}

    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))

    try:
        client.utility.verify_payment_signature(params_dict)

        # Fetch the order
        try:
            bid = Bidding.objects.get(razorpay_order_id=response['razorpay_order_id'])
        except Bidding.DoesNotExist:
            print("Order not found.")
            context.update({'status': False})
            return render(request, 'success.html', context)

        # Update order details
        bid.razorpay_payment_id = response['razorpay_payment_id']
        bid.razorpay_signature = response['razorpay_signature']
        bid.status = 'paid'
        bid.save()

        # Send email
        subject = 'Payment Successful'
        message = f"Dear {bid.designer.name},\n\n" \
                  f"Your payment for Order ID {bid.id} has been successfully processed. Thank you for choosing us!\n\n" \
                  f"Best regards,\nYour Team"
        send_mail(subject, message, 'dpoza8125@gmail.com', [bid.user.email], fail_silently=False)

        # Update context
        context.update({'status': True})
        print(context)  # Debugging context
        return render(request, 'success.html', context)

    except razorpay.errors.SignatureVerificationError:
        print("Signature verification failed.")
        context.update({'status': False})
        return render(request, 'success.html', context)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        context.update({'status': False})
        return render(request, 'success.html', context)

def showdesigners(request):
    context = checksession(request)
    if context is None:
        context = {}
    alldesigners = DesignerProfile.objects.all()
    context['alldesigner'] = alldesigners
    return render(request,'service-list.html',context)

from django.shortcuts import render, get_object_or_404
from .models import DesignerProfile, Category, Design

from django.shortcuts import render
from .models import DesignerProfile, Category, Design

import razorpay
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import DesignerProfile, Design, Category, Booking

def portfolio_view(request, designer_id):
    uid = request.session.get('log_id')
    context = checksession(request)

    # Get designer and handle errors
    try:
        designer = DesignerProfile.objects.get(id=designer_id)
    except DesignerProfile.DoesNotExist:
        messages.error(request, "Designer not found.")
        return redirect('designer_list')

    # Get available designs
    categories = Category.objects.all()
    designs = Design.objects.filter(designer=designer.user)

    if request.method == "POST":
        # Retrieve payment mode
        payment_mode = request.POST.get('payment_mode')

        # Retrieve selected designs
        selected_design_ids = request.POST.getlist('designs')
        if not selected_design_ids:
            messages.error(request, "Please select at least one design.")
            return render(request, 'portfolio.html', {
                'designer': designer,
                'categories': categories,
                'designs': designs,
            })

        selected_designs = Design.objects.filter(id__in=selected_design_ids)
        total_price = sum(design.design_price for design in selected_designs)

        if payment_mode == "online":
            # Razorpay Payment Logic
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            amount = int(total_price * 100)  # Convert to paisa
            try:
                razorpay_order = client.order.create({
                    "amount": amount,
                    "currency": "INR",
                    "receipt": f"order_{uid}",
                    "payment_capture": 1,
                })
                razorpay_order_id = razorpay_order['id']

                # Create booking for online payment
                booking = Booking.objects.create(
                    user=Login(id=uid),
                    designer=designer,
                    total_price=total_price,
                    razorpay_order_id=razorpay_order_id,
                    payment_mode='online',
                    status='pending',
                )
                booking.designs.set(selected_designs)

                # Pass Razorpay payment details to template
                context.update({
                    'razorpay_payment': {
                        'amount': amount,
                        'order_id': razorpay_order_id,
                        'key': settings.RAZORPAY_KEY_ID,
                    },
                    'designer': designer,
                    'selected_designs': selected_designs,
                    'total_price': total_price,
                })
                return render(request, 'portfolio.html', context)

            except razorpay.errors.BadRequestError as e:
                messages.error(request, f'BadRequestError: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

        elif payment_mode == "offline":
            # Offline Payment Logic
            address = request.POST.get("address")
            reference = request.POST.get("reference")
            remark = request.POST.get("remark")

            booking = Booking.objects.create(
                user=Login(id=uid),
                designer=designer,
                total_price=total_price,
                address=address,
                offline_reference=reference,
                offline_remarks=remark,
                payment_mode='offline',
                status='pending',
            )
            booking.designs.set(selected_designs)
            messages.success(request, "Offline payment details submitted successfully.")
            return redirect('showdesigners')

        else:
            messages.error(request, "Invalid payment mode selected.")

    # Update context with default data
    context.update({
        'designer': designer,
        'categories': categories,
        'designs': designs,
    })
    return render(request, 'portfolio.html', context)

from django.core.mail import send_mail

def pay_status(request):
    context = checksession(request)
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(
        auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f')
    )

    try:
        # Verify the payment signature
        client.utility.verify_payment_signature(params_dict)

        # Get the order based on the Razorpay order ID
        order = Booking.objects.get(razorpay_order_id=response['razorpay_order_id'])

        # Update the Razorpay payment ID and signature in the order
        order.razorpay_payment_id = response['razorpay_payment_id']
        order.razorpay_signature = response['razorpay_signature']

        # Set the status to 'paid' if payment is successful
        order.status = 'paid'
        order.save()

        # Send a confirmation email
        subject = 'Payment Successful'
        message = f"Dear {order.user.name},\n\n" \
                  f"Your payment for Order ID {order.id} has been successfully processed. Thank you for choosing us!\n\n" \
                  f"Best regards,\nYour Team"
        sender_email = 'dpoza8125@gmail.com'  # Replace with your sender email address
        recipient_email = [order.user.email]

        send_mail(subject, message, sender_email, recipient_email, fail_silently=False)

        context.update({'status': True})
        return render(request, 'success.html', context)

    except razorpay.errors.SignatureVerificationError:
        # Handle signature verification errors
        print("Signature verification failed.")
        return render(request, 'success.html', {'status': False})

    except Exception as e:
        # Handle other exceptions
        print(f"Error occurred: {str(e)}")
        return render(request, 'success.html', {'status': False})

def showfeedback(request):
    context = checksession(request)
    uid = request.session.get('log_id')  # Ensure user is logged in and has a session

    # Get plants associated with the user's completed cart items
    book_design = Design.objects.all()

    context.update({"designdetails": book_design})
    if request.method == 'POST':
        design_id = request.POST.get('orders')  # Plant ID from the form
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')

        # Check if the selected plant is in the user's completed cart items
        if not book_design.filter(id=design_id).exists():
            messages.error(request, "You can only give feedback for design you have completed orders for.")
            return redirect('index')

        # Check if feedback for the selected plant already exists
        if Feedback.objects.filter(design_id=design_id, user_id=uid).exists():
            messages.error(request, "You have already submitted feedback for this design.")
            return redirect('index')

        # Create feedback if all checks pass
        Feedback.objects.create(
            user=Login.objects.get(id=uid),
            design=Design.objects.get(id=design_id),
            ratings=ratings,
            comment=feedback_message,
        )

        messages.success(request, "Your feedback has been submitted successfully.")
        return redirect('index')

    return render(request, 'feedback.html', context)

def complaint_submit(request):
    context = checksession(request)
    uid = request.session['log_id']

    if request.method == "POST":
        sub = request.POST.get('subject1')
        desc = request.POST.get('description1')

        complaindata = Complaint(user=Login(id=uid),subject=sub, description=desc)
        complaindata.save()
        messages.success(request ,'your complain has been sent successfully')
        return redirect('/')

    return render(request, 'Complaint.html', context)

def booking_desinger(request):
    context = checksession(request)
    uid = request.session['log_id']

    # Filter bookings for the current user
    paymentdata = Booking.objects.filter(user_id=uid).prefetch_related('designs', 'designer__user')

    # Update context with payment details
    context.update({'bookings': paymentdata})

    return render(request, 'showdesignerbooking.html', context)

def booking_by_user(request):
    context = checksession(request)
    uid = request.session['log_id']
    # Get the gardener profile of the logged-in user
    designer = get_object_or_404(DesignerProfile, user=Login(id=uid))
    # Fetch all bookings for the gardener
    bookings = Booking.objects.filter(designer=designer).prefetch_related('designs', 'user')

    # Pass the bookings data to the template
    context.update({
        'designer': designer,
        'bookings': bookings,
    })

    return render(request, 'showuserbooking.html', context)
