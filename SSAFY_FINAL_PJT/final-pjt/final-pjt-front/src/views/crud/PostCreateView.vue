<template>
  <div class="container mt-5">
    <h2><b>게시글 생성 페이지</b></h2>
    <form @submit.prevent="createPost" class="d-flex flex-column form-control p-3 gap-2 mt-5">
      <label for="title">제목 : </label>
      <input type="text" id="title" v-model.trim="title" class="form-control">
      <label for="content">내용 : </label>
      <textarea id="content" v-model.trim="content" class="form-control"></textarea>
      <input type="submit" value="게시글 생성" class="btn btn-primary mt-3">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const postStore = usePostStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const title = ref(null)
const content = ref(null)

const createPost = function () {
  axios({
    method: 'post',
    url: `${postStore.API_URL}/api/v1/posts/`,
    data: {
      category: route.params.categoryId,
      title: title.value,
      content: content.value,
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  }).then((res) => {
    postStore.posts.unshift(res.data)
    router.replace({ name: 'PostDetailView', params: { id: res.data.id }})
  }).catch(err => console.log(err))
}
</script>

<style scoped>

</style>