import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { usePostStore } from '@/stores/post'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()
  const postStore = usePostStore()
  const token = ref(null)
  const user = ref(null)
  // 전체 user 리스트
  const userList = ref([])
  const selectedMenu = ref('home')

  const isAuthenticated = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const selectedProfilePage = ref('기본 정보 수정')

  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then(res => {
        console.log('회원가입이 완료되었습니다.')
        const password = password1
        logIn({ username, password })
      })
      .catch(err => {
        console.log(Object.values(err.response.data))
        for(let i=0; Object.values(err.response.data).length > i; i++) {
          for(let j=0; Object.values(err.response.data)[i].length > j; j++) {
            alert(Object.values(err.response.data)[i][j])
          }
        }
      })
  }

  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        token.value = res.data.key
        getUser()
        router.push({ name: 'MainView' })
      })
      .catch(err => {
        for(let i=0; Object.values(err.response.data).length > i; i++) {
          for(let j=0; Object.values(err.response.data)[i].length > j; j++) {
            alert(Object.values(err.response.data)[i][j])
          }
        }
      })
  }

  const getUser = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        user.value = res.data
      })
      .catch(err => {
        console.log(err)
        token.value = null
        router.push({ name: 'LogInView' })
        user.value = null
        postStore.clear()
      })
  }


  const getUserList = function () {
    axios ({
      method: 'get',
      url: `${API_URL}/accounts/profile/${user.value.pk}`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then ((res) => {
        // console.log(res.data)
        userList.value = res.data
      })
      .catch ((err) => {
        console.log(err)
      })
  }

  return { API_URL, token, userList, isAuthenticated, user, selectedProfilePage, signUp, logIn, getUser, getUserList, selectedMenu }
}, { persist: true })
