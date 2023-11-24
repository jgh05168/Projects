<template>
  <div>
    <h1 v-if="authStore.user" class="profile-heading m-3">{{ authStore.user.username }} 님의 프로필 페이지</h1>
    <div class="row mt-4">
      <div class="col-2">
        <p :class="{ selected: authStore.selectedProfilePage === '기본 정보 수정' }" @click="changeProfilePage('기본 정보 수정')">기본 정보 수정</p>
        <p :class="{ selected: authStore.selectedProfilePage === '비밀번호 변경' }" @click="changeProfilePage('비밀번호 변경')">비밀번호 변경</p>
        <p :class="{ selected: authStore.selectedProfilePage === '가입한 상품 정보' }" @click="changeProfilePage('가입한 상품 정보')" v-if="authStore.user && !authStore.user.is_superuser">가입한 상품 정보</p>
        <p :class="{ selected: authStore.selectedProfilePage === '상품 추천 받기' }" @click="changeProfilePage('상품 추천 받기')" v-if="authStore.user && !authStore.user.is_superuser">상품 추천 받기</p>
      </div>
      <div class="col-10">
        <div v-if="authStore.selectedProfilePage === '기본 정보 수정'" class="profile-section">
          <ProfileInfo :selectedProfilePage="authStore.selectedProfilePage"/>
        </div>
        <div v-if="authStore.selectedProfilePage === '비밀번호 변경'" class="profile-section">
          <PasswordChange :selectedProfilePage="authStore.selectedProfilePage"/>
        </div>
        <div v-if="authStore.selectedProfilePage === '가입한 상품 정보'" class="profile-section">
          <Portfolio :selectedProfilePage="authStore.selectedProfilePage" :appViewHeight="appViewHeight"/>
        </div>
        <div v-if="authStore.selectedProfilePage === '상품 추천 받기'" class="profile-section">
          <ProductRecommend :selectedProfilePage="authStore.selectedProfilePage" :appViewHeight="appViewHeight"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ProfileInfo from '@/components/profile/ProfileInfo.vue'
import PasswordChange from '@/components/profile/PasswordChange.vue'
import Portfolio from '@/components/profile/Portfolio.vue'
import ProductRecommend from '@/components/profile/ProductRecommend.vue'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  appViewHeight: Number
})

const authStore = useAuthStore()

const changeProfilePage = (page) => {
  authStore.selectedProfilePage = page
  if (page === '상품 추천 받기') {
    authStore.getUserList()
  }
}

</script>

<style scoped>
.selected {
  color: green;
  font-weight: bold;
  font-size: large;
}
.profile-section {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
}
.profile-heading {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}
.col-2 p {
  cursor: pointer;
  margin: 0;
  padding: 8px;
  border-radius: 4px;
  display: inline-block;
}
.col-2 p:hover {
  background-color: #f0f0f0;
}
.row {
  margin: 0;
}
</style>