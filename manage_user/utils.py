import logging
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import OneTimePasscode
from django.db import IntegrityError
from lebricoleur.celery import app
from django.utils import timezone
from datetime import timedelta
import string

logger = logging.getLogger(__name__)
User = get_user_model()
def generate_otp(length=6):
     return ''.join(str(random.randint(1, 9)) for _ in range(length))
  

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_otp_email(self, user):
    try:
        logger.info(f"Valeur de user reçue : {user}")

        if isinstance(user, dict):
            user_id = user.get('id')
            if not user_id:
                logger.error("L'objet user ne contient pas d'ID valide.")
                return False
            user = User.objects.filter(id=user_id).first()
            if not user:
                logger.error(f"Utilisateur avec ID {user_id} introuvable.")
                return False

        # Vérification de l'objet user
        if not isinstance(user, User):
            raise ValueError("L'objet passé n'est pas une instance de User")

        # Vérification de l'existence de l'utilisateur dans la base de données
        user_db = User.objects.filter(id=user.id).first()
        if not user_db:
            logger.error(f"L'utilisateur avec l'ID {user.id} n'existe pas en base.")
            return False

        # Vérifier s'il existe un OTP existant pour l'utilisateur
        existing_otp = OneTimePasscode.objects.filter(user=user).first()
        if existing_otp:
            logger.warning(f"Un OTP existe déjà pour l'utilisateur {user.id}. Le code sera remplacé.")

            # Mise à jour de l'OTP au lieu de le supprimer
            existing_otp.code = generate_otp()
            existing_otp.expires_at = timezone.now() + timedelta(minutes=1)  # Expiration dans 10 minutes
            existing_otp.save()
            otp_code = existing_otp.code
        else:
            # Création d'un nouveau OTP
            otp_code = generate_otp()
            otp_instance = OneTimePasscode(
                user=user,
                code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=1)  # Expiration dans 10 minutes
            )
            otp_instance.save()

        # Envoi de l'email avec le code OTP
        subject = "Code OTP pour la vérification de votre email"
        email_body = render_to_string("otp_email.html", {
            "otp": otp_code,
            "user": user,
            "current_site": "Le bricoleur Web App"
        })

        d_email = EmailMessage(subject, email_body, settings.EMAIL_HOST_USER, [user.email])
        d_email.content_subtype = "html"
        d_email.send(fail_silently=False)

        logger.info(f"OTP envoyé avec succès à {user.email}")
        return True

    except IntegrityError as e:
        logger.error(f"Erreur d'intégrité de la base de données : {str(e)}")
        return False

    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'OTP : {str(e)}")
        raise self.retry(exc=e)  # Réessayer l'envoi en cas d'échec temporaire
# import logging
# import random
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from .models import OneTimePasscode
# from django.db import IntegrityError
# from lebricoleur.celery import app


# logger = logging.getLogger(__name__)
# User = get_user_model()

# def generate_otp(length=6):
#     return ''.join(str(random.randint(1, 9)) for _ in range(length))
# @app.task
# def send_otp_email(user):
#     try:
#         logger.info(f"Valeur de user reçue : {user}")

#         # Vérification de l'utilisateur, d'abord sous forme de dict
#         if isinstance(user, dict):  
#             user_id = user.get('id')
#             if not user_id:
#                 logger.error("L'objet user ne contient pas d'ID valide.")
#                 return False
#             user = User.objects.filter(id=user_id).first()
#             if not user:
#                 logger.error(f"Utilisateur avec ID {user_id} introuvable.")
#                 return False

#         # Vérification que l'objet est bien une instance de User
#         if not isinstance(user, User):
#             raise ValueError("L'objet passé n'est pas une instance de User")

#         # Vérification de l'existence de l'utilisateur
#         user_db = User.objects.filter(id=user.id).first()
#         if not user_db:
#             logger.error(f"L'utilisateur avec l'ID {user.id} n'existe pas en base.")
#             return False

#         # Vérification si un OTP existe déjà pour cet utilisateur
#         existing_otp = OneTimePasscode.objects.filter(user=user).first()
#         if existing_otp:
#             logger.warning(f"Un OTP existe déjà pour l'utilisateur {user.id}. Le code sera remplacé.")

#         otp_code = generate_otp()

#         # Suppression de l'ancien OTP s'il existe
#         OneTimePasscode.objects.filter(user=user).delete()

#         # Création du nouvel OTP
#         otp_instance = OneTimePasscode(user=user, code=otp_code)
#         otp_instance.save()

#         # Envoi de l'email
#         subject = "Code OTP pour la vérification de votre email"
#         email_body = render_to_string("otp_email.html", {
#             "otp": otp_code,
#             "user": user,
#             "current_site": "Le bricoleur Web App"
#         })

#         d_email = EmailMessage(subject, email_body, settings.EMAIL_HOST_USER, [user.email])
#         d_email.content_subtype = "html"
#         d_email.send(fail_silently=False)

#         logger.info(f"OTP envoyé avec succès à {user.email}")
#         return True

#     except IntegrityError as e:
#         logger.error(f"Erreur d'intégrité de la base de données : {str(e)}")
#         return False

#     except Exception as e:
#         logger.error(f"Erreur lors de l'envoi de l'OTP : {str(e)}")
#         return False


# # import logging
# # import random
# # from django.core.mail import EmailMessage
# # from django.template.loader import render_to_string
# # from django.conf import settings
# # from django.contrib.auth import get_user_model
# # from .models import OneTimePasscode

# # logger = logging.getLogger(__name__)
# # User = get_user_model()

# # def generate_otp(length=6):
# #     return ''.join(str(random.randint(1, 9)) for _ in range(length))



# # def send_otp_email(user):
# #     try:
# #         logger.info(f"Valeur de user reçue : {user}")

# #         if isinstance(user, dict):  # Vérification correcte
# #             user_id = user.get('id')
# #             logger.info(f"User ID extrait : {user_id}")

# #             if user_id is None:
# #                 logger.error("L'objet user ne contient pas d'ID valide.")
# #                 return False

# #             user = User.objects.filter(id=user_id).first()
# #             if not user:
# #                 logger.error(f"Utilisateur avec ID {user_id} introuvable.")
# #                 return False

# #         if not isinstance(user, User):
# #             raise ValueError("L'objet passé n'est pas une instance de User")

# #         # Vérifier encore une fois si l'utilisateur existe
# #         user_db = User.objects.filter(id=user.id).first()
# #         if not user_db:
# #             logger.error(f"L'utilisateur avec l'ID {user.id} n'existe pas en base.")
# #             return False

# #         otp_code = generate_otp()

# #         # Suppression des anciens OTP
# #         OneTimePasscode.objects.filter(user=user).delete()

# #         # Vérification après suppression
# #         if not User.objects.filter(id=user.id).exists():
# #             logger.error(f"Après suppression de l'OTP, l'utilisateur {user.id} a disparu !")
# #             return False

# #         # Création du nouvel OTP
# #         otp_instance = OneTimePasscode(user=user, code=otp_code)
# #         otp_instance.save()

# #         # Envoi de l'email
# #         subject = "Code OTP pour la vérification de votre email"
# #         email_body = render_to_string("otp_email.html", {
# #             "otp": otp_code,
# #             "user": user,
# #             "current_site": "SimpRH Web App"
# #         })

# #         d_email = EmailMessage(subject, email_body, settings.EMAIL_HOST_USER, [user.email])
# #         d_email.content_subtype = "html"
# #         d_email.send(fail_silently=False)

# #         logger.info(f"OTP envoyé avec succès à {user.email}")
# #         return True

# #     except Exception as e:
# #         logger.error(f"Erreur lors de l'envoi de l'OTP : {str(e)}")
# #         return False



