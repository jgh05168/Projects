<template>
  <!-- <div style="position: fixed !important; width: 86%; height: 88%; left: 7%; bottom: 2%;">
    <div data-vbg-autoplay="true" data-vbg="https://youtu.be/hzfXLHR0psg?si=DWvkbqW7WD6vfx3W"></div>
  </div> -->
  <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel" data-bs-interval="5000">
    <div class="carousel-inner">
      <div class="carousel-item active">
        <div class="m1_img d-block w-100 full-width-height d-flex flex-column align-items-center justify-content-center">
          <h2 class="content font animate__animated animate__rotateInDownLeft">더 나은 내일을 위한 금융 선택, 지금 시작하세요.</h2>
          <div class="my-3">
            <RouterLink v-if="authStore.user" :to="{ name: 'ProductCompareView' }" class="btn btn-outline-dark content font btn-lg" :class="{ selected: authStore.seletedMenu === 'compare' }" @click="changeMenu('compare')">함께 하러 가기</RouterLink>
            <RouterLink v-else :to="{ name: 'LogInView' }" class="btn btn-outline-dark content font btn-lg" :class="{ selected: authStore.seletedMenu === 'login' }" @click="changeMenu('login')">함께 하러 가기</RouterLink>
          </div>
        </div>
      </div>
      <div class="carousel-item ">
        <div class="m2_img d-block w-100 full-width-height d-flex flex-column align-items-center justify-content-center">
          <h2 class="content font animate__animated animate__zoomIn">최적의 상품을 여러분들께 제공 해 드립니다.</h2>
          <div class="my-3">          
            <RouterLink v-if="authStore.user" :to="{ name: 'ProductCompareView' }" class="btn btn-outline-dark content font btn-lg" :class="{ selected: authStore.seletedMenu === 'compare' }" @click="changeMenu('compare')">함께 하러 가기</RouterLink>
            <RouterLink v-else :to="{ name: 'LogInView' }" class="btn btn-outline-dark content font btn-lg" :class="{ selected: authStore.seletedMenu === 'login' }" @click="changeMenu('login')">함께 하러 가기</RouterLink>
          </div>
        </div>
      </div>
      <div class="carousel-item ">
        <div class="m3_img d-block w-100 full-width-height d-flex flex-column align-items-center justify-content-center">
          <h2 class="content font">여러분의 목표에 맞는 최고의 금융 상품을 탐색해보세요.</h2>
          <div class="my-3 animate__animated animate__zoomIn animate__delay-1s">          
            <RouterLink v-if="authStore.user" :to="{ name: 'ProductCompareView' }" class="btn btn-outline-dark content font btn-lg" :class="{ selected: authStore.seletedMenu === 'compare' }" @click="changeMenu('compare')">함께 하러 가기</RouterLink>
            <RouterLink v-else :to="{ name: 'LogInView' }" class="btn btn-outline-dark content font btn-lg" :class="{ selected: authStore.seletedMenu === 'login' }" @click="changeMenu('login')">함께 하러 가기</RouterLink>
          </div>
        </div>
      </div>

      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const changeMenu = (menu) => {
  authStore.seletedMenu = menu
}

$(document).ready(function() {
  $('[data-vbg]').youtube_background()
})
</script>

<style scoped>

.full-width-height {
  width: 100%;
  height: 100%;
}

.full-width-height img {
  width: 100%;
  height: 100%;
}

.carousel-item {
    height: 94.41vh; /* 이미지를 창 전체 높이로 표시할 수 있도록 설정 */
  }

.carousel-item img {
  object-fit: cover; /* 이미지가 부모 요소에 맞게 조정되도록 설정 */
  width: 100%;
  height: 100%;
}

.m1_img {
  position: relative;
}

.m1_img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/main1.jpg");
  background-size: cover;
  opacity: 0.4;
  z-index: auto;
}

.m2_img {
  position: relative;
}

.m2_img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/main2.jpg");
  background-size: cover;
  opacity: 0.4;
  z-index: auto;
}


.m3_img {
  position: relative;
}

.m3_img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/main3.jpg");
  background-size: cover;
  opacity: 0.4;
  z-index: auto;
}

.content {
  position: relative;
  z-index: 1;
}

@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700&display=swap');

.font {
  font-family: 'Nanum Myeongjo', serif;
}


.get_height {
    height: 100vh; /* Set the height to 100% of viewport height */
}

.selected {
  font-weight: bold;
  font-size: large;
}
</style>