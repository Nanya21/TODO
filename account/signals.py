from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.core.mail import send_mail


# @receiver(post_save, sender=CustomUser)

# def post_save_generate_code(sender, instance, created, *args, **kwargs):
#     if created:

#         pass

def send_activation_email(sender, instance, created,**kwargs):
    
    if created:
        message = f"""Hello, {instance.first_name}.
Thank you for signing up on our platform. We are very glad🤗
Regards,
The Django Team.
        """
        
        send_mail(subject="Your Account Has Been Created", 
                  message=message,
                  recipient_list=[instance.email],
                  from_email="ekohifunaya@gmail.com")