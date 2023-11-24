<template>
  <div v-if="post" class="mt-3 mx-3">
    <h5>[{{ post.category.name }}] {{ post.title }}</h5>
    <hr>
    <div class="d-flex justify-content-between">
      <p v-if="post.category.name !== '익명게시판'">작성자 : <b>{{ post.user.username }}</b></p>
      <p v-else>작성자 : 익명</p>
      <div>
        <p class="text-secondary smallfont">작성일 : {{ formatDate(post.created_at) }} / 수정일 : {{ formatDate(post.updated_at) }}</p>
      </div>
    </div>

    <div class="d-flex justify-content-between">
      <div class="col me-3">
        {{ post.content }}
      </div>
      <div class="d-flex flex-column justify-content-end">
        <div :class="{'mb-3': isMyPost}">
          <span class="me-2">좋아요 : {{ likeCount }} </span>
          <i @click.prevent="likePost(post.id)" class="bi fs-5" :class="{ 'bi-hand-thumbs-up': !isLike, 'bi-hand-thumbs-up-fill': isLike }"></i>
        </div>
        <div v-if="isMyPost" class="d-flex column-gap-2">
          <button @click.prevent="goPostUpdate(post.id)" class="btn btn-outline-success btn-sm" >수정</button>
          <button @click.prevent="postDelete(post.id)" class="btn btn-outline-danger btn-sm">삭제</button>
        </div>
      </div>
    </div>
    <hr>

    <div class="comment mt-3">
      <Comment :post="post"/>
    </div>
  </div>
</template>

<script setup>
import Comment from '@/components/Comment.vue'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostStore } from '@/stores/post'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const postStore = usePostStore()
const post = ref(null)

const isLike = ref(false)

const likePost = function (postId) {
  postStore.like(postId)
  getPost()
}

const likeCount = computed (() => {
  return post.value.like_users.length
})

const isMyPost = computed (() => {
  return authStore.user.pk === post.value.user.pk
})

const formatDate = function (dateTime) {
  return moment(dateTime).format('YYYY-MM-DD HH:mm:ss')
}

const goPostUpdate = function (postId) {
  router.push({ name: 'PostUpdateView', params: { id: postId}})
}

const postDelete = (postId) => {
  axios({
    method: 'delete',
    url: `${postStore.API_URL}/api/v1/posts/${postId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      const itemIdx = postStore.posts.findIndex((item) => item.id === postId)
      postStore.posts.splice(itemIdx, 1)
      router.push({ name: 'CommunityView' })
    })
    .catch((err) => {
      console.log(err)
    }) 
}

const getPost = function () {
  axios({
    method: 'get',
    url: `${postStore.API_URL}/api/v1/posts/${route.params.id}/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      post.value = res.data
      postStore.getComments(post.value.id)
      isLike.value = post.value.like_users.includes(authStore.user.pk) ? true : false
    })
    .catch((err) => {
      console.log(err)
    })
}

onMounted(() => {
  getPost()
  // isLike.value = post.value.like_users.includes(authStore.user.id) ? true : false
})
</script>

<style scoped>
p {
  margin: auto 0;
  margin-bottom: 1.2rem;
}
.smallfont {
  margin: auto 0;
  font-size: 12px;
}
</style>