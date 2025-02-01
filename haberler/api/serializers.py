from rest_framework import serializers
from haberler.models import Makale

from datetime import datetime, date

from django.utils.timesince import timesince

class MakaleSerilizer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    
    class Meta:
        model = Makale
        fields = '__all__'
        # fields = ['yazar', 'baslik', 'metin']
        # exclude = ['yazar', 'baslik', 'metin'] # Hariç Tutar bu başlıkları
        read_only_fields = ['id', 'yaratilma_tarihi', 'güncellenme_tarihi']
        
    def get_time_since_pub(self, object):
        now = datetime.now()
        pub_date = object.yayımlanma_tarihi
        if object.aktif == True:        
            time_delta = timesince(pub_date, now)
            return time_delta
        else:
            return 'Aktif Değil'
    
    def validate_yayımlanma_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Yayımlanma tarihi ileri bir tarih olamaz')
        return tarihdegeri
        
        
        








####### STANDART SERIALIZER #######
class MakaleDefaultSerilizer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayımlanma_tarihi = serializers.DateField( )
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only = True)
    güncellenme_tarihi = serializers.DateTimeField(read_only = True)
    
    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayımlanma_tarihi = validated_data.get('yayımlanma_tarihi', instance.yayımlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Başlık ve açıklama alanları aynı olamaz. Lütfen farklı bir açıklama giriniz.')
        return data
    
    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Başlık 20 karakterden azdır. Sizin Başlığınız {len(value)} karakter uzunluğunda. Daha uzun bir başlık giriniz.')
        return value