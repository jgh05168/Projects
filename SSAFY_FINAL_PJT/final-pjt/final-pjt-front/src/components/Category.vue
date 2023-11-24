<template>
  <div>
    <div v-if="category">
      <div class="d-flex justify-content-between">
        <h2><i class="bi bi-justify"></i> {{ category.name }}</h2>
        <div v-if="category.name === '공지사항' && authStore.user.is_superuser">
          <button class="btn btn-outline-primary" @click.prevent="goPostCreate()">게시글 작성</button>
        </div>
        <div v-else-if="category.name !== '공지사항'">
          <button class="btn btn-outline-primary" @click.prevent="goPostCreate()">게시글 작성</button>
        </div>
      </div>
      <hr>
      <div :style="{ maxHeight: dynamicMaxHeight + 'px', overflowY: 'auto'}">
        <div v-if="category.name !== '공지사항' && noticePosts.length !== 0" class="me-3">
          <div v-for="post in noticePosts" :key="post">
            <p class="ms-2">
              <b>[공지사항] </b>
              <b @click.prevent="goDetail(post.id)">{{ post.title }}</b>
            </p>
          </div>
          <hr class="line-margin">
        </div>
        <div class="me-3">
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th scope="col">순번</th>
                <th v-if="category.name !== '익명게시판'" scope="col">작성자</th>
                <th v-else scope="col"></th>
                <th scope="col">제목</th>
                <th scope="col">추천 수</th>
                <th scope="col">작성일</th>
              </tr>
            </thead>
            <tbody v-if="category.name !== '전체게시판'">
              <tr v-for="(post, index) in filteredPosts" :key="post.id" @click.prevent="goDetail(post.id)">
                <th scope="row">{{ getCategoryPostIndex(index) }}</th>
                <td v-if="category.name !== '익명게시판'">{{ post.user.username }}</td>
                <td v-else></td>
                <td>{{ post.title }}</td>
                <td>{{ post.like_users.length }}</td>
                <td>{{ formatDate(post.updated_at) }}</td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr v-for="(post, index) in exceptNoticePosts" :key="post" @click.prevent="goDetail(post.id)">
                <th scope="row">{{ exceptNoticePosts.length - index }}</th>
                <td>{{ post.user.username }}</td>
                <td>{{ post.title }}</td>
                <td>{{ post.like_users.length }}</td>
                <td>{{ formatDate(post.updated_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else>
      <h2><i class="bi bi-alexa text-warning"></i> 커뮤니티</h2>
      <hr>
      <div class="text-center mt-5">
        <h4>게시판을 적극 이용해주세요!</h4>
        <img src="@/assets/춘식.png" alt="" class="mt-5 animate__animated animate__bounce">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostStore } from '@/stores/post'

const props = defineProps({
  category: Object,
  appViewHeight: Number
})

const router = useRouter()
const authStore = useAuthStore()
const postStore = usePostStore()

const filteredPosts = ref([])
const noticePosts = ref([])
const exceptNoticePosts = ref([])

const goPostCreate = function () {
  router.push({ name: 'PostCreateView', params: { categoryId: props.category.id }})
}

const goDetail = function (postId) {
  router.push({ name: 'PostDetailView', params: { id: postId }})
}

const getCategoryPosts = function (categoryId) {
  return postStore.posts.filter(post => post.category.id === categoryId)
}

const getCategoryPostIndex = function (index) {
  return filteredPosts.value.length - index
}

const updateFilteredPosts = function (categoryId) {
  if (postStore.posts) {
    filteredPosts.value = getCategoryPosts(categoryId)
  }
}

const formatDate = function (dateTime) {
  const formattedDate = new Date(dateTime)
  return formattedDate.toISOString().split('T')[0]
}

const dynamicMaxHeight = ref(0)

onMounted(() => {
  dynamicMaxHeight.value = props.appViewHeight * 0.8
  if ( props.category ) {
    updateFilteredPosts(props.category.id)
  }
  if (postStore.posts) {
    noticePosts.value = postStore.posts.filter(post => post.category.name === '공지사항')
    exceptNoticePosts.value = postStore.posts.filter(post => post.category.name !== '공지사항')
  }
})

watch(() => postStore.posts, () => {
  if (props.category) {
    updateFilteredPosts(props.category.id)
    if (postStore.posts) {
      noticePosts.value = postStore.posts.filter(post => post.category.name === '공지사항')
      exceptNoticePosts.value = postStore.posts.filter(post => post.category.name !== '공지사항')
    }
  }
})
</script>

<style scoped>
.line-margin {
  margin-bottom: 0;
}
.table th, td {
  width: 10%;
  text-align: center;
  padding: 8px 0;
}
.table th:nth-child(1) {
  width: 5%;
}
.table th:nth-child(3) {
  width: 40%;
}
img {
  width: 18rem;
}
</style>