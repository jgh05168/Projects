<script setup>
import { onMounted, computed, ref, nextTick } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import BankNearbyView from './views/BankNearbyView.vue'
const snowfallImagePath = '@/assets/christmas.gif'


const authStore = useAuthStore()
const route = useRoute();
const pageHeight = ref('')
const router = useRouter();


const isBankNearbyView = function () {
  const ans = route.name === 'BankNearbyView'
  return ans}

const isMainView = function () {
const ans = route.name === 'MainView'
return ans}

const needContainerClass = () => {return isBankNearbyView() || isMainView()}

const setPageHeight = () => {
  const windowHeight = window.innerHeight
  pageHeight.value = `${windowHeight}px`
}

const appView = ref(null)
const appViewHeight = ref(0)

const goToMain = () => {
  router.push({ name : 'MainView'})
}

const changeMenu = (menu) => {
  authStore.seletedMenu = menu
}

onMounted(async () => {
  if (authStore.user) {
    authStore.getUser()
  }
  setPageHeight()
  window.addEventListener('resize', setPageHeight)

  await nextTick()
  appViewHeight.value = appView.value.clientHeight
})

</script>

<template>
  <div class="background-with-gif" :style="{height: pageHeight}">
    <header>
      <nav v-if="authStore.user && authStore.isAuthenticated" :class="{ 'd-flex': true, 'justify-content-center': true, 'mb-3': !needContainerClass()}" style="background-color: #E6E6E6;">
        <img src="@/assets/logo.png" alt="" width="50" height="50" @click.prevent="goToMain" :class="{ selected: authStore.seletedMenu === 'home' }" @click="changeMenu('home')">
        <RouterLink :to="{ name: 'MainView' }" class="nav-link" :class="{ selected: authStore.seletedMenu === 'home' }" @click="changeMenu('home')">Home</RouterLink>
        <RouterLink :to="{ name: 'ProfileView', params: { id: authStore.user.pk } }" :class="{ selected: authStore.seletedMenu === 'profile' }" @click="changeMenu('profile')">프로필</RouterLink>
        <RouterLink :to="{ name: 'ProductCompareView' }" :class="{ selected: authStore.seletedMenu === 'compare' }" @click="changeMenu('compare')">금융상품 비교</RouterLink>
        <RouterLink :to="{ name: 'CurrencyCalculationView' }" :class="{ selected: authStore.seletedMenu === 'currency' }" @click="changeMenu('currency')">환율 계산</RouterLink>
        <RouterLink :to="{ name: 'BankNearbyView' }" :class="{ selected: authStore.seletedMenu === 'search' }" @click="changeMenu('search')">근처 은행 검색</RouterLink>
        <RouterLink :to="{ name: 'CommunityView' }" :class="{ selected: authStore.seletedMenu === 'comunity' }" @click="changeMenu('comunity')">게시판</RouterLink>
        <RouterLink v-if="authStore.user.is_superuser" :to="{ name: 'CategoryCreateView' }" :class="{ selected: authStore.seletedMenu === 'categorycreate' }" @click="changeMenu('categorycreate')">게시판 목록 생성</RouterLink>
      </nav>
      <nav v-else class="d-flex justify-content-center" style="background-color: #E6E6E6;" :class="{'mb-3': !needContainerClass()}">
        <img src="@/assets/logo.png" alt="" width="50" height="50" @click.prevent="goToMain" :class="{ selected: authStore.seletedMenu === 'home' }" @click="changeMenu('home')">
        <RouterLink :to="{ name: 'MainView' }" :class="{ selected: authStore.seletedMenu === 'home' }" @click="changeMenu('home')">Home</RouterLink>
        <RouterLink :to="{ name: 'SignUpView' }" :class="{ selected: authStore.seletedMenu === 'signup' }" @click="changeMenu('signup')">회원가입</RouterLink>
        <RouterLink :to="{ name: 'LogInView' }" :class="{ selected: authStore.seletedMenu === 'login' }" @click="changeMenu('login')">로그인</RouterLink>
      </nav>
    </header>
    <div :class="{ container: !needContainerClass(), bd: !needContainerClass() }" :style="{backgroundColor: 'white'}" ref="appView">
      <RouterView :appViewHeight="appViewHeight"/>
    </div>
  </div>
</template>

<style scoped>

.background-with-gif {
  background-image: url('@/assets/christmas.gif');
  background-size: cover;
  z-index: -1;
}


nav {
  margin: 0 auto;
  gap: 30px;
  line-height: 300%;
}

nav a {
  color: black;
}

a {
  text-decoration: none;
  color: white;
}
.bd {
  border: 3px solid rgba(150, 128, 170, 0.5);
  padding: 0%;
  border-radius: 15px;
  height: 90%;
}

.selected {
  font-weight: bold;
  font-size: large;
}
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Cute+Font&family=Gothic+A1:wght@500&family=Nanum+Gothic&display=swap');

* {
  font-family: 'Gothic A1', sans-serif;
}
</style>