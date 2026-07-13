from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # 1. Buni qo'shdik
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TizimSozlamasi, FoydalanuvchiProfil, Davomat, HarakatTarixi


# 1. Boshliq/Ustoz ko'radigan asosiy Xarita sahifasi
@login_required(login_url='login')  # 2. Kirmagan odamni shartta siz yaratgan login'ga otadi
def dashboard_view(request):
    return render(request, 'dashboard.html')


# 2. Ishchi/O'quvchi ko'radigan sodda boshqaruv sahifasi
def mobil_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'mobil.html')


# 3. Tizimga kirish (Login) sahifasi mantiqi
def login_view(request):
    # Agar foydalanuvchi oldin kirgan bo'lsa, shundoq xaritaga (dashboardga) o'tib ketadi
    if request.user.is_authenticated:
        return redirect('dashboard')  # 3. 'mobil' edi, 'dashboard'ga o'zgartirdik (Instagramdek)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Login yoki parol xato!'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


class LokatsiyaYangilashAPI(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Avtorizatsiyadan o'tilmagan"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            profil = user.profil
        except FoydalanuvchiProfil.DoesNotExist:
            return Response({"error": "Profil topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        is_mock = request.data.get('is_mock_location', False)
        oflayn_nuqtalar = request.data.get('oflayn_nuqtalar', [])

        if is_mock:
            return Response({"error": "Fake GPS taqiqlangan!"}, status=status.HTTP_400_BAD_REQUEST)

        if oflayn_nuqtalar:
            tarix_obunachilari = []
            for nuqta in oflayn_nuqtalar:
                tarix_obunachilari.append(HarakatTarixi(
                    profil=profil,
                    latitude=nuqta['latitude'],
                    longitude=nuqta['longitude'],
                    vaqt=nuqta['vaqt']
                ))
            HarakatTarixi.objects.bulk_create(tarix_obunachilari)

        if lat and lng:
            profil.joriy_latitude = lat
            profil.joriy_longitude = lng
            profil.save()

        return Response({"status": "Muvaffaqiyatli yangilandi"}, status=status.HTTP_200_OK)


class XaritaMalumotlariAPI(APIView):
    def get(self, request):
        sozlama = TizimSozlamasi.objects.first()
        rejim = sozlama.rejim if sozlama else 'biznes'
        bugun = timezone.now().date()

        aktiv_profillar = []
        profillar = FoydalanuvchiProfil.objects.all()

        for p in profillar:
            davomat = Davomat.objects.filter(profil=p, sana=bugun).first()
            status_text = davomat.status if davomat else 'kelmadi'

            if rejim == 'talim' and status_text == 'keldi':
                continue

            if p.oxirgi_yangilanish:
                if (timezone.now() - p.oxirgi_yangilanish).total_seconds() > 900:
                    onlayn_status = "oflayn"
                else:
                    onlayn_status = "onlayn"
            else:
                onlayn_status = "oflayn"

            rasm_url = p.rasm.url if p.rasm else "/static/default_avatar.png"

            aktiv_profillar.append({
                "id": p.id,
                "ism": p.ism,
                "telefon": p.telefon,
                "rasm": rasm_url,
                "lat": float(p.joriy_latitude) if p.joriy_latitude else None,
                "lng": float(p.joriy_longitude) if p.joriy_longitude else None,
                "status": status_text,
                "aloqa": onlayn_status,
                "vaqt_boshlanishi": p.vaqt_boshlanishi.strftime("%H:%M") if p.vaqt_boshlanishi else "09:00",
                "vaqt_yakuni": p.vaqt_yakuni.strftime("%H:%M") if p.vaqt_yakuni else "18:00"
            })

        return Response({"rejim": rejim, "majliz": aktiv_profillar})