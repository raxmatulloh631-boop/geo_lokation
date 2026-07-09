from django.contrib import admin
from .models import TizimSozlamasi, FoydalanuvchiProfil, Davomat, HarakatTarixi

@admin.register(TizimSozlamasi)
class TizimSozlamasiAdmin(admin.ModelAdmin):
    list_display = ['rejim']

@admin.register(FoydalanuvchiProfil)
class FoydalanuvchiProfilAdmin(admin.ModelAdmin):
    list_display = ['ism', 'telefon', 'vaqt_boshlanishi', 'vaqt_yakuni', 'oxirgi_yangilanish']
    search_fields = ['ism', 'telefon']

@admin.register(Davomat)
class DavomatAdmin(admin.ModelAdmin):
    list_display = ['profil', 'sana', 'status']
    list_filter = ['status', 'sana']

@admin.register(HarakatTarixi)
class HarakatTarixiAdmin(admin.ModelAdmin):
    list_display = ['profil', 'latitude', 'longitude', 'vaqt']
    list_filter = ['profil', 'vaqt']