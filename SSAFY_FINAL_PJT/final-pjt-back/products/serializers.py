from rest_framework import serializers
from .models import Bank, DepositProduct, Deposit, SavingProduct, Saving


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'


class DepositProductSerializer(serializers.ModelSerializer):
    deposit_set = DepositSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = '__all__'


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'


class SavingProductSerializer(serializers.ModelSerializer):
    saving_set = SavingSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = '__all__'

