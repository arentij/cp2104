from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Shard
from django.contrib.admin.views.decorators import staff_member_required
import qrcode
from io import BytesIO
import base64

# Create your views here.


def shard_detail(request, shard_uuid):
    shard = get_object_or_404(Shard, uuid=shard_uuid)
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'shard_detail.html', {'shard': shard})
    elif shard.password:
        if request.method == 'POST':
            entered_password = request.POST.get('password')
            if entered_password == shard.password:
                return render(request, 'shard_detail.html', {'shard': shard})
            else:
                return render(request, 'password_prompt.html', {'shard_uuid': shard_uuid, 'error': 'Incorrect password'})
        else:
            return render(request, 'password_prompt.html', {'shard_uuid': shard_uuid})
    else:
        return render(request, 'shard_detail.html', {'shard': shard})

@staff_member_required
def shard_list(request):
    shards = Shard.objects.all()
    shard_data = []
    for shard in shards:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        shard_url = request.build_absolute_uri(f"/shard/{shard.uuid}/")
        qr.add_data(shard_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        shard_data.append({
            'uuid': shard.uuid,
            'name': shard.name,
            'password': shard.password,
            'qr_code': qr_code_base64,
            'url': shard_url,
        })
    return render(request, 'shard_list.html', {'shard_data': shard_data})