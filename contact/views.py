from .serializers import ContactFormSerializer
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
logger = logging.getLogger(__name__)

# Contact Form API View
class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            message = serializer.validated_data['message']

            subject = f"Contact Form Submission from {name}"
            email_message = f"""
            Name : {name}
            Email : {email}
            Phone : {phone}

            Message:
            {message.strip()}
            """.strip()

            try:
                send_mail(
                    subject,
                    email_message,
                    settings.EMAIL_HOST_USER, 
                    ['recipient@example.com'],
                    fail_silently=False,
                )

                # লগ করা
                logger.info(f"Email sent successfully from {email} (Phone: {phone})")

                return Response({"message": "Email Sent Successfully!"}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Email sending failed: {repr(e)}") 
                return Response(
                    {"error": f"Failed to send email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )