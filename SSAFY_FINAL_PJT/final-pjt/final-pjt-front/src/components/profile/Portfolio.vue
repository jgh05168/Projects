<template>
  <div>
    <h2>{{ selectedProfilePage }}</h2>
    <hr>
    <div class="container" :style="{ maxHeight: dynamicMaxHeight + 'px', overflowY: 'auto'}">
      <div class="row">
        <div class="col-2">
          <p><b>가입한 상품 목록</b></p>
        </div>
        <div class="col-10">
          <div v-if="authStore.user.financial_products">
            <div v-for="(product, index) in myProduct" :key="product.fin_prdt_cd" >
              <p>
                {{ index + 1 }} : 
                <b>{{ product.fin_prdt_nm.includes('예금') ? '(정기예금)' : '(정기적금)' }}</b>
                {{ product.kor_co_nm }} - 
                <span @click.prevent="goProductDetail(product.fin_prdt_nm, product)" class="text-primary" :class="{ selected: authStore.seletedMenu === 'compare' }" @click="changeMenu('compare')">{{ product.fin_prdt_nm }}</span>
              </p>
            </div>
          </div>
          <div v-else>
            <p><b>가입한 상품이 없습니다</b></p>
          </div>
        </div>
      </div>
    
      <div class="row mt-3">
        <div class="col-2">
          <p><b>가입한 상품 금리</b></p>
        </div>
        <div class="col-10">
          <div v-if="authStore.user.financial_products">
            <hr>
            <Bar :data="chartData" :options="chartOptions" />
          </div>
          <div v-else>
            <p @click.prevent="goProductCompare">
              <i class="bi bi-bank2 text-secondary"></i> <b>금융상품을 저장해주세요</b>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProductStore } from '@/stores/product'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)


const props = defineProps({
  selectedProfilePage: String,
  appViewHeight: Number
})

const router = useRouter()
const authStore = useAuthStore()
const productStore = useProductStore()

const myProduct = ref([])

const changeMenu = (menu) => {
  authStore.seletedMenu = menu
}

const goProductCompare = function () {
  router.push({ name: 'ProductCompareView' })
}

const goProductDetail = function (productTitle, product) {
  const selectedProduct = product.fin_prdt_nm.includes('예금') ? "정기예금" : "정기적금"
  router.push({ name: 'ProductDetailView', params: { name: productTitle}, query: { type: selectedProduct }})
}

// 차트 생성
const getProductName = function (prdt_cds) {
  let productInfo = null
  let productName = ['평균 금리']

  if (prdt_cds) {
    prdt_cds.split(',').forEach(element => {
      productInfo = productStore.all_products.filter(item => item.fin_prdt_cd === element)
      productName.push(productInfo[0].fin_prdt_nm)
    })
  }
  return productName
}
  
const getIntrRate = function() {
  let temp_list = []
  if (authStore.user.financial_products) {
    authStore.user.financial_products.split(',').forEach(element => {
      let maxInterestRate = Number.NEGATIVE_INFINITY
      const foundProduct = productStore.all_products.find(item => item.fin_prdt_cd === element)
      if (foundProduct.deposit_set) {
        foundProduct.deposit_set.forEach(element => {
          if (element.intr_rate > maxInterestRate) {
            maxInterestRate = element.intr_rate
          }
        })
        temp_list.push(maxInterestRate)
      } else {
        foundProduct.saving_set.forEach(element => {
          if (element.intr_rate > maxInterestRate) {
            maxInterestRate = element.intr_rate
          }
        })
        temp_list.push(maxInterestRate)
      }
    })
  }

  // 최대 금리 평균 구하기
  const sum = temp_list.reduce((accumulator, currentValue) => accumulator + currentValue, 0)
  const average = sum / temp_list.length
  temp_list.unshift(average)

  console.log(temp_list)
  return temp_list
}


const getIntrRate2 = function() {
  let temp_list = []
  if (authStore.user.financial_products) {
    authStore.user.financial_products.split(',').forEach(element => {
      const foundProduct = productStore.all_products.find(item => item.fin_prdt_cd === element)
      let maxInterestRate = Number.NEGATIVE_INFINITY
      if (foundProduct.deposit_set) {
        foundProduct.deposit_set.forEach(element => {
          if (element.intr_rate2 > maxInterestRate) {
            maxInterestRate = element.intr_rate2
          }
        })
        temp_list.push(maxInterestRate)
      } else {
        foundProduct.saving_set.forEach(element => {
          if (element.intr_rate2 > maxInterestRate) {
            maxInterestRate = element.intr_rate2
          }
        })
        temp_list.push(maxInterestRate)
      }
    })
  }
  
  // 최대 금리 평균 구하기
  const sum = temp_list.reduce((accumulator, currentValue) => accumulator + currentValue, 0)
  const average = sum / temp_list.length
  temp_list.unshift(average)
  console.log(temp_list)

  return temp_list
}

const chartData = {
  labels: getProductName(authStore.user.financial_products),
  datasets: [
    {
      label: '저축 금리',
      backgroundColor: '#f879',
      data: getIntrRate(),
      borderColor: 'skyblue',
    },
    {
      label: '최고 우대 금리',
      backgroundColor: '#f1322',
      data: getIntrRate2(),
      borderColor: 'green',
    },
  ],
}

const chartOptions = { responsive: true, maintainAspectRatio: true }

const dynamicMaxHeight = ref(0)

onMounted(() => {
  dynamicMaxHeight.value = props.appViewHeight * 0.70
  const productCodes = ref()
  if (authStore.user.financial_products) {
    productCodes.value = authStore.user.financial_products === null ? '' : authStore.user.financial_products.split(',').map(code => code.trim())
  }
  if (productCodes.value) {
    productCodes.value.forEach(code => {
      myProduct.value.push(productStore.all_products.find(item => item.fin_prdt_cd === code))
    })
  }
})
</script>

<style scoped>
.selected {
  font-weight: bold;
  font-size: large;
}
</style>