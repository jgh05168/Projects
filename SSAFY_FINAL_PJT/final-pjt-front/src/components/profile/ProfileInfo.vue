<template>
  <div>
    <h2>{{ selectedProfilePage }}</h2>
    <hr>
    <div v-if="authStore.user" class="row">
      <div class="col-2">
        <p><b>회원번호</b></p>
        <p><b>ID</b></p>
        <p><b>Email</b></p>
        <p><b>닉네임</b></p>
        <p><b>나이</b></p>
        <p><b>현재 가진 금액</b></p>
        <p><b>연봉</b></p>

      </div>
      <div class="col-10">
        <p>{{ authStore.user.pk }}</p>
        <p>{{ authStore.user.username }}</p>
        <div class="d-flex justify-content-between">
          <p v-if="authStore.user.email">{{ authStore.user.email }}</p>
          <p v-else>이메일을 설정해주세요</p>
          <ProfileUpdateModal :fieldName="'email'" @update-profile="updateProfile"/>
        </div>
        <div class="d-flex justify-content-between">
          <p v-if="authStore.user.nickname">{{ authStore.user.nickname }}</p>
          <p v-else>닉네임을 설정해주세요</p>
          <ProfileUpdateModal :fieldName="'nickname'" @update-profile="updateProfile"/>
        </div>
        <div class="d-flex justify-content-between">
          <p v-if="authStore.user.age">{{ authStore.user.age }}</p>
          <p v-else>나이를 입력해주세요</p>
          <ProfileUpdateModal :fieldName="'age'" @update-profile="updateProfile"/>
        </div>
        <div class="d-flex justify-content-between">
          <p v-if="authStore.user.money">{{ formattedMoney }} 원</p>
          <p v-else>현재 가진 금액을 입력해주세요</p>
          <ProfileUpdateModal :fieldName="'money'" @update-profile="updateProfile"/>
        </div>
        <div class="d-flex justify-content-between">
          <p v-if="authStore.user.salary">{{ formattedSalary }} 만원</p>
          <p v-else>연봉을 입력해주세요</p>
          <ProfileUpdateModal :fieldName="'salary'" @update-profile="updateProfile"/>
        </div>
      </div>
    </div>
      
    <div class="text-center mt-4">
      <button @click.prevent="logout" class="btn btn-outline-danger me-3">로그아웃</button>
      <!-- 회원탈퇴 모달 -->
      <button class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#userDelete">
        회원탈퇴
      </button>
      <div class="modal fade" id="userDelete" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">회원탈퇴</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              회원탈퇴 하시겠습니까 ?
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
              <button @click.prevent="signout" class="btn btn-danger" data-bs-dismiss="modal">확인</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 회원탈퇴 모달 -->
      <div v-if="authStore.user && authStore.user.is_superuser">
        <hr>
        <button @click.prevent="loadData" class="btn btn-outline-secondary">예적금 데이터 업데이트</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import ProfileUpdateModal from '@/components/profile/ProfileUpdateModal.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useProductStore } from '@/stores/product'
import { useCurrencyRateStore } from '@/stores/currency'
import axios from 'axios'

const props = defineProps({
  selectedProfilePage: String
})

const router = useRouter()
const authStore = useAuthStore()
const productStore = useProductStore()
const currencyStore = useCurrencyRateStore()

// 회원정보 수정
const formatNumber = function (value) {
  // 정규표현식 사용 -> 천 단위 쉼표 추가
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const formattedMoney = ref(authStore.user.money ? formatNumber(authStore.user.money) : '')
const formattedSalary = ref(authStore.user.salary ? formatNumber(authStore.user.salary) : '')

const updateProfile = function () {
  authStore.getUser()
  formattedMoney.value = formatNumber(authStore.user.money)
  formattedSalary.value = formatNumber(authStore.user.salary)

}

const logout = function () {
  axios({
    method: 'post',
    url: `${authStore.API_URL}/accounts/logout/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(res => {
      console.log('로그아웃 되었습니다.')
      authStore.token = null
      authStore.user = null
      router.replace({ name: 'MainView' })
    })
    .catch(err => console.log(err))
}

const signout = function () {
  axios({
    method: 'delete',
    url: `${authStore.API_URL}/accounts/signout/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(res => {
      console.log('회원 탈퇴가 완료되었습니다.')
      authStore.token = null
      authStore.user = null
      router.replace({ name: 'MainView' })
    })
    .catch(err => console.log(err))
}

const loadData = function () {
  axios({
    method: 'get',
    url: `${authStore.API_URL}/api/v1/save_products_db/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(res => {
      console.log('예적금 상품데이터가 성공적으로 업데이트되었습니다.')
      productStore.getBanks()
      productStore.getDepositProduct()
      productStore.getDepositOption()
      productStore.getSavingProduct()
      productStore.getSavingOption()
      productStore.total_products()
      
    })
    .catch(err => console.log(err))
}
</script>

<style scoped>
p {
  margin: auto 0;
}
.col-2, .col-10 {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.row {
  margin: 0;
}
</style>