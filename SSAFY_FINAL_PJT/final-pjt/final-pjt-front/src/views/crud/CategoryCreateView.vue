<template>
  <div class="d-flex flex-column align-items-center justify-content-center" style="height: 100%;">
    <div class="categoryForm rounded p-4 mb-3">
      <form @submit.prevent="createCategory">
        <label for="category">Category 종류:</label><br>
        <input type="text" id="category" class="form-control my-3" placeholder="카테고리를 입력해주세요." v-model="name">
        <input type="submit" value="카테고리 생성" class="btn btn-primary">
      </form>
    </div>
    <img src="@/assets/춘식댄스.png" alt="" class="animate__animated animate__shakeX">
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router';

const name = ref(null)
const postStore = usePostStore()
const authStore = useAuthStore()
const router = useRouter()

const createCategory = function () {
  axios({
    method: 'post',
    url: `${postStore.API_URL}/api/v1/category/create/`,
    data: {
      name: name.value,
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  }).then((res) => {
    postStore.category.push(res.data)
    router.push({ name: 'CommunityView' })
  }).catch(err => console.log(err))
}
</script>

<style scoped>
.categoryForm {
  margin: 0 auto;
  border: 1px solid rgba(128, 128, 128, 0.3);
  width: 50%;
}

input {
  border: 1px solid rgba(128, 128, 128, 0.3);
  width: 100%;
}
img {
  width: 18rem;
}
</style>