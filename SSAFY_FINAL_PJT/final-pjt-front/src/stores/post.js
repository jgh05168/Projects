import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

export const usePostStore = defineStore('post', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const authStore = useAuthStore()
  const category = ref([])
  const posts = ref([])
  const comments = ref(null)
  const selectedCategory = ref(null)

  const getCategory = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/category/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        category.value = res.data
      })
      .catch(err => console.log('category가 없습니다'))
  }

  const getPosts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/posts/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        posts.value = res.data.slice().reverse()
      })
      .catch(err => {
        console.log('post가 없습니다')
        posts.value = []
      })
  }

  const getComments = function (post_pk) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/posts/${post_pk}/comments/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        comments.value = res.data
      })
      .catch(err => console.log(err))
  }

  const clear = function () {
    category.value = []
    posts.value = []
    comments.value = null
    selectedCategory.value = null
  }

  const like = function (post_pk) {
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/posts/${post_pk}/like/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        const itemIdx = posts.value.findIndex((item) => item.id === post_pk )
        posts[itemIdx] = res.data
      })
      .catch(err => console.log(err))
  }

  return { posts, category, comments, API_URL, selectedCategory, getPosts, getCategory, getComments, clear, like }
}, { persist: true })
