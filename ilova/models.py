from django.db import models
from django.contrib.auth.models import User


class TizimSozlamasi(models.Model):
    """ Tizim firma uchunmi yoki maktab uchunmi — shuni belgilaydi """
    REJIM_CHOICES = [
        ('biznes', 'Kompaniya / Ishchilar'),
        ('talim', 'O\'quv markazi / O\'quvchilar'),  # Apostrof xatosi to'g'rilandi
    ]
    rejim = models.CharField(max_length=20, choices=REJIM_CHOICES, default='biznes')

    def __str__(self):
        return f"Joriy rejim: {self.get_rejim_display()}"


class FoydalanuvchiProfil(models.Model):
    """ Ishchi yoki O'quvchining shaxsiy profili """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    ism = models.CharField(max_length=100, verbose_name="Ismi familyasi")
    telefon = models.CharField(max_length=20, verbose_name="Telefon raqami")
    rasm = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Rasm (Avatar)")

    # Jonli koordinatalar (oxirgi kelgan nuqtasi)
    joriy_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    joriy_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    oxirgi_yangilanish = models.DateTimeField(auto_now=True)

    # Superadmin belgilaydigan majburiy ish/dars vaqtlari
    vaqt_boshlanishi = models.TimeField(default="08:00:00", verbose_name="Boshlanish vaqti")
    vaqt_yakuni = models.TimeField(default="17:00:00", verbose_name="Tugash vaqti")

    def __str__(self):
        return self.ism


class Davomat(models.Model):
    """ Kunlik davomat va kuzatuv statusi """
    STATUS_CHOICES = [
        ('keldi', 'Keldi / Kuzatish shartmas'),
        ('kelmadi', 'Kelmagan / Qidirilmoqda'),
    ]
    profil = models.ForeignKey(FoydalanuvchiProfil, on_delete=models.CASCADE, related_name='davomatlari')
    sana = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='kelmadi')

    def __str__(self):
        return f"{self.profil.ism} - {self.sana} - {self.status}"


class HarakatTarixi(models.Model):
    """ Oflayn paytda telefonda saqlanib, keyin serverga yuklangan koordinatalar tarixi """
    profil = models.ForeignKey(FoydalanuvchiProfil, on_delete=models.CASCADE, related_name='tarixi')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    vaqt = models.DateTimeField(verbose_name="GPS olingan vaqt")

    class Meta:
        ordering = ['vaqt']