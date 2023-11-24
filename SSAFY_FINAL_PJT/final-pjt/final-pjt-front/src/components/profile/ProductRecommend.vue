<template>
  <div>
    <div v-if="authStore.user.age && authStore.user.money && authStore.user.salary">
      <h2>{{ selectedProfilePage }}</h2>
      <hr>
      <!-- 상품 추천 모달 -->
      <div class="m-3">
        <button class="btn btn-outline-warning col-12" data-bs-toggle="modal" data-bs-target="#userDelete" @click="productStore.recommendProducts()">
            상품 추천 받기
        </button>
      </div>
      <div class="modal fade" id="userDelete" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">상품 추천 받기</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              상품 추천 완료
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="productStore.recommand_list" :style="{ maxHeight: dynamicMaxHeight + 'px', overflowY: 'auto' }">
        <div v-for="(product, index) in productStore.recommand_list">
          <div class="d-flex">
            <p class="me-3 ms-3">{{ index + 1 }}</p>
            <p class="ms-2 col-5">{{ product.products }}</p>
            <p class="col-4" @click="goProductDetail(product.kor_nm)">{{ product.kor_nm}}</p>
            <button type="button" class=" ms-2 btn btn-outline-primary btn-sm" @click="goProductDetail(product.kor_nm)" :class="{ selected: authStore.seletedMenu === 'compare' }" @click.prevent="changeMenu('compare')">상세정보</button>
          </div>
          <hr>
        </div>
      </div>
      <div v-else>
        <p>추천 상품 없음</p>
      </div>
    </div>

    <div v-else>
      <div class="alert alert-warning text-center" role="alert">
        <p>개인 상세 정보(나이, 현재 가진 금액, 연봉)를 입력한 뒤 이용이 가능합니다.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProductStore } from '@/stores/product'
import axios from 'axios'

const props = defineProps({
  selectedProfilePage: String,
  appViewHeight: Number
})

const router = useRouter()
const authStore = useAuthStore()
const productStore = useProductStore()

const changeMenu = (menu) => {
  authStore.seletedMenu = menu
}

const goProductDetail = function (productTitle) {
  const selectedProduct = productStore.all_products.find(item => item.fin_prdt_nm === productTitle).fin_prdt_nm.includes('예금') ? "정기예금" : "정기적금"
  router.push({ name: 'ProductDetailView', params: { name: productTitle}, query: { type: selectedProduct }})
}

const dynamicMaxHeight = ref(0)

onMounted(() => {
  dynamicMaxHeight.value = props.appViewHeight * 0.62
})

</script>

<style scoped>
p {
  margin: auto 0;
}
.modal-body {
  margin: 10px auto;
  font-weight: bold;
  font-size: large;
}
.selected {
  font-weight: bold;
  font-size: large;
}
</style>