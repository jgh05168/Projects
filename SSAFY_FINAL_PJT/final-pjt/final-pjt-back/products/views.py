import requests
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django.shortcuts import get_list_or_404
from .models import DepositProduct, Deposit, Saving, SavingProduct, Bank
from .serializers import BankSerializer, DepositProductSerializer, DepositSerializer, SavingProductSerializer, SavingSerializer


# 본인의 API KEY 로 수정합니다.
api_key = settings.API_KEY

# 요구사항에 맞도록 이곳의 코드를 수정합니다.
deposit_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
saving_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'

# Create your views here.
@api_view(['GET'])
def deposit_and_saving_list(request):
    deposit_list, deposit_product_list = get_deposit_products(deposit_url)
    saving_list, saving_product_list = get_saving_products(saving_url)

    for product_info in deposit_product_list:
        if not Bank.objects.filter(name=product_info.get('kor_co_nm')):
            bank = Bank()
            bank.name = product_info.get('kor_co_nm')
            bank.save()

        if not DepositProduct.objects.filter(fin_prdt_cd=product_info['fin_prdt_cd']):
            deposit_product = DepositProduct()
            deposit_product.fin_prdt_cd = product_info.get('fin_prdt_cd')  # 'fin_prdt_cd' 키의 값을 가져와 fin_prdt_cd 필드에 할당합니다.
            deposit_product.fin_prdt_nm = product_info.get('fin_prdt_nm') 
            deposit_product.kor_co_nm = product_info.get('kor_co_nm') 
            deposit_product.bank = Bank.objects.get(name=product_info.get('kor_co_nm'))
            deposit_product.dcls_month = product_info.get('dcls_month')
            deposit_product.dcls_strt_day = product_info.get('dcls_strt_day')
            deposit_product.dcls_end_day = product_info.get('dcls_end_day')
            deposit_product.join_deny = product_info.get('join_deny')
            deposit_product.join_way = product_info.get('join_way')
            deposit_product.spcl_cnd = product_info.get('spcl_cnd')
            deposit_product.save()

            for deposit_info in deposit_list:
                # print(deposit_info)
                # print('------------------')
                if deposit_info['fin_prdt_cd'] == deposit_product.fin_prdt_cd:
                    deposit = Deposit()
                    deposit.deposit_product = deposit_product
                    deposit.intr_rate = deposit_info.get('intr_rate')
                    deposit.save_trm = deposit_info.get('save_trm')
                    deposit.intr_rate_type = deposit_info.get('intr_rate_type')
                    deposit.intr_rate_type_nm = deposit_info.get('intr_rate_type_nm')
                    deposit.intr_rate2 = deposit_info.get('intr_rate2')
                    deposit.save()

    # 적금 상품
    for product_info in saving_product_list:
        if not Bank.objects.filter(name=product_info.get('kor_co_nm')):
            bank = Bank()
            bank.name = product_info.get('kor_co_nm')
            bank.save()

        if not SavingProduct.objects.filter(fin_prdt_cd=product_info['fin_prdt_cd']):
            saving_product = SavingProduct()
            saving_product.fin_prdt_cd = product_info.get('fin_prdt_cd')  # 'fin_prdt_cd' 키의 값을 가져와 fin_prdt_cd 필드에 할당합니다.
            saving_product.fin_prdt_nm = product_info.get('fin_prdt_nm') 
            saving_product.kor_co_nm = product_info.get('kor_co_nm') 
            saving_product.bank = Bank.objects.get(name=product_info.get('kor_co_nm'))
            saving_product.dcls_month = product_info.get('dcls_month')
            saving_product.dcls_strt_day = product_info.get('dcls_strt_day')
            saving_product.dcls_end_day = product_info.get('dcls_end_day')
            saving_product.join_deny = product_info.get('join_deny')
            saving_product.join_way = product_info.get('join_way')
            saving_product.spcl_cnd = product_info.get('spcl_cnd')
            saving_product.save()

            for saving_info in saving_list:
                # print(saving_info)
                # print('------------------')
                if saving_info['fin_prdt_cd'] == saving_product.fin_prdt_cd:
                    saving = Saving()
                    saving.saving_product = saving_product
                    saving.intr_rate = saving_info.get('intr_rate')
                    saving.save_trm = saving_info.get('save_trm')
                    saving.intr_rate_type = saving_info.get('intr_rate_type')
                    saving.intr_rate_type_nm = saving_info.get('intr_rate_type_nm')
                    saving.intr_rate2 = saving_info.get('intr_rate2')
                    saving.rsrv_type = saving_info.get('rsrv_type')
                    saving.rsrv_type_nm = saving_info.get('rsrv_type_nm')
                    saving.save()

    
    return Response({'message': 'update complete!'})


@api_view(['GET'])
def exchange_rate(request):
    exchange_api_key = settings.EXCHANGE_API_KEY
    now = datetime.now()

    # 원하는 형식으로 날짜 포맷 지정하기 (yymmdd)
    formatted_date = now.strftime("%Y%m%d")
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={exchange_api_key}&searchdate={formatted_date}&data=AP01'

    response = requests.get(url).json()

    return Response(response)





def get_deposit_products(url):

  # 응답을 JSON 형태로 변환
    response = requests.get(url).json()

    key = response['result'].keys()
    baseList = response['result']['baseList']       # 상품리스트
    optionList = response['result']['optionList']   # 옵션리스트

    new_dict = []
    for base in baseList:       # 상품리스트 순회
        deposit_product = {}    # 금융상품별 딕셔너리       
        deposit_product['fin_prdt_cd'] = base['fin_prdt_cd']
        deposit_product['fin_prdt_nm'] = base['fin_prdt_nm']
        deposit_product['kor_co_nm'] = base['kor_co_nm']
        deposit_product['dcls_month'] = base['dcls_month']
        deposit_product['dcls_strt_day'] = base['dcls_strt_day']
        deposit_product['dcls_end_day'] = base['dcls_end_day']
        deposit_product['join_deny'] = base['join_deny']
        deposit_product['join_way'] = base['join_way']
        deposit_product['spcl_cnd'] = base['spcl_cnd']
        new_dict.append(deposit_product)        # 금융상품별 딕셔너리 취합하여 새로운 리스트 생성

    product_info = []
    for option in optionList:       # 옵션리스트 순회
      option_dict = {}            # 옵션별 금리 정보
      option_dict['fin_prdt_cd'] = option['fin_prdt_cd']
      option_dict['intr_rate'] = option['intr_rate']       # 옵션별 금리 정보 추가
      option_dict['save_trm'] = option['save_trm']
      option_dict['intr_rate_type'] = option['intr_rate_type']
      option_dict['intr_rate_type_nm'] = option['intr_rate_type_nm']
      option_dict['intr_rate2'] = option['intr_rate2']
      # print(deposit_info)
      product_info.append(option_dict)        # 옵션별 금리 정보 취합하여 금융상품별 금리 정보 생성

    return product_info, new_dict



def get_saving_products(url):

  # 응답을 JSON 형태로 변환
    response = requests.get(url).json()

    key = response['result'].keys()
    baseList = response['result']['baseList']       # 상품리스트
    optionList = response['result']['optionList']   # 옵션리스트

    new_dict = []
    for base in baseList:       # 상품리스트 순회
        saving_product = {}    # 금융상품별 딕셔너리        
        saving_product['fin_prdt_cd'] = base['fin_prdt_cd']
        saving_product['fin_prdt_nm'] = base['fin_prdt_nm']
        saving_product['kor_co_nm'] = base['kor_co_nm']
        saving_product['dcls_month'] = base['dcls_month']
        saving_product['dcls_strt_day'] = base['dcls_strt_day']
        saving_product['dcls_end_day'] = base['dcls_end_day']
        saving_product['join_deny'] = base['join_deny']
        saving_product['join_way'] = base['join_way']
        saving_product['spcl_cnd'] = base['spcl_cnd']
        new_dict.append(saving_product)        # 금융상품별 딕셔너리 취합하여 새로운 리스트 생성

    product_info = []
    for option in optionList:       # 옵션리스트 순회
      option_dict = {}            # 옵션별 금리 정보
      option_dict['fin_prdt_cd'] = option['fin_prdt_cd']
      option_dict['intr_rate'] = option['intr_rate']       # 옵션별 금리 정보 추가
      option_dict['save_trm'] = option['save_trm']
      option_dict['intr_rate_type'] = option['intr_rate_type']
      option_dict['intr_rate_type_nm'] = option['intr_rate_type_nm']
      option_dict['intr_rate2'] = option['intr_rate2']
      option_dict['rsrv_type'] = option['rsrv_type']
      option_dict['rsrv_type_nm'] = option['rsrv_type_nm']
      # print(deposit_info)
      product_info.append(option_dict)        # 옵션별 금리 정보 취합하여 금융상품별 금리 정보 생성

    return product_info, new_dict


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank(request):
    banks = get_list_or_404(Bank)
    serializer = BankSerializer(banks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def depositproduct(request):
    depositproducts = get_list_or_404(DepositProduct)
    serializer = DepositProductSerializer(depositproducts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deposit(request):
    deposits = get_list_or_404(Deposit)
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def savingproduct(request):
    savingproducts = get_list_or_404(SavingProduct)
    serializer = SavingProductSerializer(savingproducts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saving(request):
    savings = get_list_or_404(Saving)
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

