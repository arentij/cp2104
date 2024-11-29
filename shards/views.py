from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Shard

# Create your views here.

def shard_detail(request, shard_uuid):
    shard = get_object_or_404(Shard, uuid=shard_uuid)
    if shard.password:
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
