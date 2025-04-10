# from django.test import TestCase
# from django.urls import reverse
# from .models import ServicePost, ServiceRequest
# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.core.files.uploadedfile import SimpleUploadedFile

# from manage_user.models import Technician  # Ajouté ici

# User = get_user_model()

# from manage_user.models import Technician

# class ServicePostTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         # Étape 1 : créer un utilisateur de base
#         user = User.objects.create_user(
#             email='pamelfichieu31@gmail.com',
#             password='password',
#             first_name='Technician',
#             last_name='Pamel'
#         )

#         # Étape 2 : transformer ce user en technicien (via relation OneToOne ou héritage multi-table)
#         self.technician = Technician.objects.create(user_ptr=user)

#         self.client.force_authenticate(user=self.technician)

#         self.service_post = ServicePost.objects.create(
#             title='Test Post',
#             description='This is a test post.',
#             technician=self.technician,
#             photo=SimpleUploadedFile(
#                 name='test_image.jpg',
#                 content=b'file_content',
#                 content_type='image/jpeg'
#             )
#         )
