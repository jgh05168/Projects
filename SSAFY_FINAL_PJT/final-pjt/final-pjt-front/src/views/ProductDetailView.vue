<template>
  <div class="mt-3 mx-5">
    <h2 class="mt-4"><i class="bi bi-building text-secondary"></i> 금융상품 상세 정보</h2>
    <div class="row mt-4">
      <div class="col-3">
        <p><b>공시 제출일</b></p>
        <p><b>금융회사명</b></p>
        <p><b>상품명</b></p>
        <p><b>가입제한</b></p>
        <p><b>가입방법</b></p>
        <p><b>우대조건</b></p>
      </div>
      <div class="col-9">
        <p>{{ product.dcls_month }}</p>
        <p>{{ product.kor_co_nm }}</p>
        <p>{{ product.fin_prdt_nm }}</p>
        <p>{{ join_deny }}</p>
        <p>{{ product.join_way }}</p>
        <div>
          <p v-for="condition in getSplitString(product.spcl_cnd)" :key="condition">{{ condition }}</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-3">
        <p><b>기간 별 투자 수익</b></p>
      </div>
      <div class="col-9">
        <div class="row">
          <div class="col-4">
            <select v-model="select_month" class="form-control">
              <option value="" disabled selected>기간을 선택하세요</option>
              <option v-for="option_set in product.deposit_set ? product.deposit_set : product.saving_set">{{ option_set.save_trm }}개월</option>
            </select>
          </div>
          <div class="col-4">
            <input type="text" v-model="property" class="form-control">
          </div>
          <button class="btn btn-secondary btn-fixed-size" @click="calculateBenefit()">계산</button>
        </div>
        <div class="mt-3">
          <p>저축 금리 유형 : {{ ben_type }}</p>
          <p>계산 결과 : {{ benefit }} 원</p>
        </div>
      </div>
    </div>
    <button @click.prevent="saveProduct" :disabled="!productExists" class="offset-3 btn btn-success">금융상품 저장</button>
    <button @click.prevent="deleteProduct(product.fin_prdt_cd)" :disabled="productExists" class="ms-3 btn btn-danger">금융상품 삭제</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useProductStore } from '@/stores/product'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const authStore = useAuthStore()
const productStore = useProductStore()
const product = ref([])
const join_deny = ref('')
const select_month = ref('')
const property = ref(null)
const benefit = ref(null)
const ben_type = ref('')

const productCodes = ref()

// 금융상품 삭제
const deleteProduct = function (code) {
  productCodes.value = authStore.user.financial_products === null ? '' : authStore.user.financial_products.split(',').map(code => code.trim())
  const filteredCodes = productCodes.value.filter(item => item !== code)
  const resultString = filteredCodes.join(',') ? filteredCodes.join(',') : null

  axios({
    method: 'post',
    url: `${authStore.API_URL}/accounts/profile/update/${authStore.user.pk}/`,
    data: {
      username: authStore.user.username,
      financial_products: resultString
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(res => {
      console.log(`금융상품 정보가 삭제되었습니다.`)
      authStore.user = { ...authStore.user, financial_products: res.data.financial_products }
    })
    .catch(err => console.log(err))
}

// 금융상품 저장,삭제버튼 disabled 지정
const productExists = computed(() => {
  const productCodes = authStore.user.financial_products === null ? '' : authStore.user.financial_products.split(',').map(code => code.trim())
  return productCodes.value === '' || !productCodes.includes(product.value.fin_prdt_cd)
})

// 우대조건 split
const getSplitString = function (spcl_cnd) {
  return spcl_cnd ? spcl_cnd.split('\n').map(condition => condition.trim()) : []
}

// 금융상품 저장
const saveProduct = function () {
  productCodes.value = authStore.user.financial_products === null ? '' : authStore.user.financial_products.split(',').map(code => code.trim())
  let updateCodes = ''
  if (productCodes === '' || !productCodes.value.includes(product.value.fin_prdt_cd)) {
    updateCodes = productCodes.value === '' ? product.value.fin_prdt_cd : authStore.user.financial_products + "," + product.value.fin_prdt_cd
    axios({
      method: 'post',
      url: `${authStore.API_URL}/accounts/profile/update/${authStore.user.pk}/`,
      data: {
        username: authStore.user.username,
        financial_products: updateCodes
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        console.log(`금융상품 정보가 등록되었습니다.`)
        authStore.user = { ...authStore.user, financial_products: res.data.financial_products }
        productCodes.value = authStore.user.financial_products === null ? '' : authStore.user.financial_products.split(',').map(code => code.trim())
        console.log(authStore.user.financial_products)
      })
      .catch(err => console.log(err))
  } else {
    console.log(`금융상품 정보가 이미 등록되어있습니다.`)
  }
}


const calculateBenefit = function() {
  if (!select_month) {
    window.alert('기간을 선택하세요!')
  } else {
    const option_sets = product.value.deposit_set ? product.value.deposit_set : product.value.saving_set
    const option = option_sets.find(item => item.save_trm == parseInt(select_month.value))
    ben_type.value = option.intr_rate_type_nm
    if (option.intr_rate_type_nm === '복리') {
      benefit.value = (property.value * Math.pow((1 + (option.intr_rate / 100) / 1), 1 * parseInt(select_month.value) / 30)).toFixed(2)
    }
    benefit.value = (property.value * (option.intr_rate / 100) * parseInt(select_month.value) / 30).toFixed(2)
  }
}

onMounted(() => {
  if (route.query.type === '정기예금') {
    product.value = productStore.deposit_product.find((item) => item.fin_prdt_nm === route.params.name)
  } else {
    product.value = productStore.saving_product.find((item) => item.fin_prdt_nm === route.params.name)
  }
  if (product.value.join_deny === 1){
    join_deny.value = '제한없음'
  } else if (product.value.join_deny === 2) {
    join_deny.value = '서민전용'
  } else {
    join_deny.value = '일부제한'
  }
})
</script>

<style scoped>
.btn-fixed-size {
  width: 75px;
}
</style>