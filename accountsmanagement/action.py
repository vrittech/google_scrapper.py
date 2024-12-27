# from booking.models import DestinationBook
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from accounts.models import CustomUser
# from accountsmanagement.views import send_booking_confirmation_email


# @receiver(post_save, sender=DestinationBook)
# def booking_created_handler(sender, instance, created, **kwargs):
#     if created:
#         # Construct the verification URL
#         site_url = 'https://example.com'  
#         verify_url = f"{site_url}/user-verification-success?pk={urlsafe_base64_encode(force_bytes(instance.pk))}"

#         # Fetch the admin email from the User model
#         admin_user = CustomUser.objects.filter(is_superuser=True).first()
#         if admin_user:
#             admin_name = admin_user.first_name
#             admin_email = admin_user.email
#         else:
#             raise ValueError("Admin email not found.")

#         # Send the confirmation email
#         subject = 'Booking Verification Email'
#         send_booking_confirmation_email(instance.email, verify_url, subject, instance, admin_email, admin_name)

