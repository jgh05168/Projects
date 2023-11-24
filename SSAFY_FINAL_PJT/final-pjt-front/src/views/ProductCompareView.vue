<template>
  <div class="mt-3 mx-3">
    <div class="d-flex column-gap-2">
      <p :class="{ selected: selectedProduct === '정기예금' }" @click="changeProduct('정기예금')">정기예금</p>
      <p :class="{ selected: selectedProduct === '정기적금' }" @click="changeProduct('정기적금')">정기적금</p>
    </div>
    <div class="row offset-lg-2 d-inline-block">
      <h1>{{ selectedProduct }}</h1>
    </div>
    <div class="row">
      <div class="col-12 col-lg-2">
        <div class="search-bar">
          <h3>검색하기</h3>
          <p class="text-secondary"><b>검색 조건을 입력하세요</b></p>
          <hr>
        </div>
        <label for="banks">은행 선택:</label>
        <select v-model="selectedBank" id="banks" class="form-control mb-3">
          <option value="">전체은행</option>
          <option v-for="item in productStore.banks" :key="item.name">{{ item.name }}</option>
        </select>
        <label for="term">예치 기간:</label>
        <select v-model="selectedTerm" id="term" class="form-control mb-3">
          <option value="">전체기간</option>
          <option v-for="item in ['6개월', '12개월', '24개월', '36개월']">{{ item }}</option>
        </select>
        <div class="d-flex flex-column">  
          <button @click.prevent="submitProduct" class="btn btn-info text-light">확인</button>
        </div>
      </div>
      <div class="col-12 col-lg-9 mb-3" >
        <div class="table-responsive" :style="{ maxHeight: dynamicMaxHeight + 'px', overflowY: 'auto' }">
          <table class="table table-striped">
            <thead>
              <tr>
                <th scope="col">공시 제출일</th>
                <th scope="col">금융회사명</th>
                <th scope="col">상품명</th>
                <th scope="col" v-if="term === '' || term === '6개월'">6개월 <i @click.prevent="sortTable('6개월')" class="bi bi-chevron-bar-expand"></i></th>
                <th scope="col" v-if="term === '' || term === '12개월'">12개월 <i @click.prevent="sortTable('12개월')" class="bi bi-chevron-bar-expand"></i></th>
                <th scope="col" v-if="term === '' || term === '24개월'">24개월 <i @click.prevent="sortTable('24개월')" class="bi bi-chevron-bar-expand"></i></th>
                <th scope="col" v-if="term === '' || term === '36개월'">36개월 <i @click.prevent="sortTable('36개월')" class="bi bi-chevron-bar-expand"></i></th>
              </tr>
            </thead>
            <tbody v-if="selectedProduct === '정기예금'" >
              <tr v-for="product in selectedProductList" :key="product.fin_prdt_nm">
                <td>{{ product.dcls_month }}</td>
                <td>{{ product.kor_co_nm }}</td>
                <td @click.prevent="goProductDetail(product.fin_prdt_nm, selectedProduct)">{{ product.fin_prdt_nm }}</td>
                <td v-if="term === '' || term === '6개월'">{{ save_term_Deposit(product, 6) }}</td>
                <td v-if="term === '' || term === '12개월'">{{ save_term_Deposit(product, 12) }}</td>
                <td v-if="term === '' || term === '24개월'">{{ save_term_Deposit(product, 24) }}</td>
                <td v-if="term === '' || term === '36개월'">{{ save_term_Deposit(product, 36) }}</td>
              </tr>
            </tbody>
            <tbody v-else-if="selectedProduct === '정기적금'">
              <tr v-for="product in selectedProductList" :key="product.fin_prdt_nm">
                <td>{{ product.dcls_month }}</td>
                <td>{{ product.kor_co_nm }}</td>
                <td @click.prevent="goProductDetail(product.fin_prdt_nm, selectedProduct)">{{ product.fin_prdt_nm }}</td>
                <td v-if="term === '' || term === '6개월'">{{ save_term_Saving(product, 6) }}</td>
                <td v-if="term === '' || term === '12개월'">{{ save_term_Saving(product, 12) }}</td>
                <td v-if="term === '' || term === '24개월'">{{ save_term_Saving(product, 24) }}</td>
                <td v-if="term === '' || term === '36개월'">{{ save_term_Saving(product, 36) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useProductStore } from '@/stores/product'
import { useRouter } from 'vue-router'

const props = defineProps({
  appViewHeight: Number
})

// 디테일 페이지 이동
const router = useRouter()
const goProductDetail = function (productTitle, selectedProduct) {
  router.push({ name: 'ProductDetailView', params: { name: productTitle}, query: { type: selectedProduct }})
}

const productStore = useProductStore()
const selectedBank = ref('')  // 선택한 은행
const selectedTerm = ref('')  // 선택한 기간
const term = ref('')  // 검색 이후 computed 적용을 위한 기간
const selectedProduct = ref('정기예금')  // '정기예금' or '정기적금'

const depositProduct = ref([])
const savingProduct = ref([])
const selectedProductList = ref([])

// 상품 변경
const changeProduct = (product) => {
  selectedProduct.value = product
  if (selectedProduct.value === '정기예금') {
    selectedProductList.value = depositProduct.value
  } else {
    selectedProductList.value = savingProduct.value
  }
  selectedBank.value = ''
  selectedTerm.value = ''
  term.value = ''
}

// 검색하기
const submitProduct = function () {
  // 은행별 검색
  if (selectedBank.value) {
    const bankId = productStore.banks.find((item) => item.name === selectedBank.value).id
    if (selectedProduct.value === '정기예금') {
      selectedProductList.value = depositProduct.value.filter((item) => item.bank === bankId)
    } else {
      selectedProductList.value = savingProduct.value.filter((item) => item.bank === bankId)
    }
  } else {
    if (selectedProduct.value === '정기예금') {
      selectedProductList.value = depositProduct.value
    } else {
      selectedProductList.value = savingProduct.value
    }
  }
  // 기간별 검색
  if (selectedTerm.value) {
    term.value = selectedTerm.value
  } else {
    term.value = ''
  }
}

const save_term_Deposit = computed(() => {
  return (product, term) => product.deposit_set.find((item) => item.save_trm === term) ? product.deposit_set.find((item) => item.save_trm === term).intr_rate : '-'
})

const save_term_Saving = computed(() => {
  return (product, term) => product.saving_set.find((item) => item.save_trm === term) ? product.saving_set.find((item) => item.save_trm === term).intr_rate : '-'
})

// 정렬
const sortedBase = ref(false) // 오름차순, 내림차순 전환

const sortTable = function (column) {
  sortedBase.value = !sortedBase.value

  selectedProductList.value.sort((a, b) => {
    const aValue = getValueToSort(a, column)
    const bValue = getValueToSort(b, column)
    return sortedBase.value ? bValue - aValue : aValue - bValue
  })
}

const getValueToSort = (product, column) => {
  switch (column) {
    case '6개월':
      return getSaveTermValue(product, 6)
    case '12개월':
      return getSaveTermValue(product, 12)
    case '24개월':
      return getSaveTermValue(product, 24)
    case '36개월':
      return getSaveTermValue(product, 36)
    default:
      return 0
  }
}

const getSaveTermValue = (product, term) => {
  if (selectedProduct.value === '정기예금') {
    const termValue = product.deposit_set.find((item) => item.save_trm === term)
    return termValue ? termValue.intr_rate : 0
  } else {
    const termValue = product.saving_set.find((item) => item.save_trm === term)
    return termValue ? termValue.intr_rate : 0
  }
}

const dynamicMaxHeight = ref(0)

// 초기화
onMounted(() => {
  dynamicMaxHeight.value = props.appViewHeight * 0.65
  depositProduct.value = [...productStore.deposit_product]
  savingProduct.value = [...productStore.saving_product]
  selectedProductList.value = depositProduct.value
})
</script>

<style scoped>
.selected {
  color: green;
  font-weight: bold;
}

@media (max-width: 992px) {
  .search-bar {
    display: none;
  }
}
.table th:nth-child(1), td:nth-child(1) {
  width: 10%;
  text-align: center;
}
.table th:nth-child(2), td:nth-child(2) {
  width: 10%;
  text-align: center;
}
.table th:nth-child(3), td:nth-child(3) {
  width: 40%;
  text-align: center;
}
.table th:nth-child(4), td:nth-child(4) {
  width: 6%;
  text-align: center;
}
.table th:nth-child(5), td:nth-child(5) {
  width: 6%;
  text-align: center;
}
.table th:nth-child(6), td:nth-child(6) {
  width: 6%;
  text-align: center;
}
.table th:nth-child(7), td:nth-child(7) {
  width: 6%;
  text-align: center;
}
</style>