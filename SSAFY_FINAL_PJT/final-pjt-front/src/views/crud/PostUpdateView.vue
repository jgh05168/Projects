<template>
  <div class="container mt-5">
    <h2><b>게시글 수정 페이지</b></h2>
    <form @submit.prevent="updatePost" class="d-flex flex-column form-control p-3 gap-2 mt-5">
      <label for="title">제목 : </label>
      <input type="text" id="title" v-model.trim="title" class="form-control">
      <label for="content">내용 : </label>
      <textarea id="content" v-model.trim="content" class="form-control"></textarea>
      <input type="submit" value="게시글 수정" class="btn btn-primary mt-3">
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const postStore = usePostStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const post = ref(null)
const title = ref(null)
const content = ref(null)

const updatePost = function () {
  axios({
    method: 'put',
    url: `${postStore.API_URL}/api/v1/posts/${post.value.id}/`,
    data: {
      title: title.value,
      content: content.value
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  }).then((res) => {
    postStore.posts.find(item => item.id === res.data.id).title = res.data.title
    postStore.posts.find(item => item.id === res.data.id).content = res.data.content
    router.replace({ name: 'PostDetailView', params: { id: post.value.id } })
  }).catch(err => console.log(err))
}

onMounted(() => {
  axios({
    method: 'get',
    url: `${postStore.API_URL}/api/v1/posts/${route.params.id}/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      post.value = res.data
      title.value = res.data.title
      content.value = res.data.content
    })
    .catch((err) => {
      console.log(err)
    })
})
</script>

<style scoped>

</style>