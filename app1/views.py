from django.urls import reverse
import datetime
import jwt
from django.conf import settings
from django.shortcuts import render
from app1.models import Teacher
from django.http import HttpResponse
from reportlab.pdfgen import canvas
# Create your views here.

def dataview(request):
    teacher=Teacher.objects.all()
    return render(request, "app1/data.html", {"teacher":teacher})

def generate_certificate(request, teacher_id):
    teacher=Teacher.objects.get(id=teacher_id)
    # print(teacher)
    students=[i.name for i in teacher.students.all()]
    # print(students)

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    certificate_data = {
        'teacher_name': teacher.name,
        'students': students,
        'exp': expiration_time
    }

    jwt_token = jwt.encode(certificate_data, settings.SECRET_KEY, algorithm='HS256')
    # print(jwt_token)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=certificate_{teacher.id}.pdf'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f'Certificate of Teacher-Students Pair')
    p.drawString(100, 780, f'Teacher: {teacher.name}')
    p.drawString(100, 760, f'Students: {", ".join(students)}')

    verify_certificate_url = reverse('verify_certificate', args=[jwt_token])
    # print(verify_certificate_url)
    p.linkURL(f"http://localhost:8000{verify_certificate_url}", (100, 740, 300, 760), relative=1)
    p.setFillColorRGB(0, 0, 1)
    p.drawString(100, 740, 'Verify Certificate')
    p.showPage()
    p.save()

    return response


def verify_certificate(request, token):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return HttpResponse("Valid Certificate")
    except jwt.ExpiredSignatureError:
        return HttpResponse("Certificate has expired.")
    except jwt.InvalidTokenError:
        return HttpResponse("Invalid certificate token.")
