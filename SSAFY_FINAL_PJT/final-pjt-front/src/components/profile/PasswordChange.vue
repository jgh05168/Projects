<template>
  <div>
    <h2>{{ selectedProfilePage }}</h2>
    <hr>
    <form @submit.prevent="changePassword" class="d-flex flex-column form-control p-3 gap-2">
      <label for="new_password1"><b>New Password : </b></label>
      <input type="password" id="new_password1" v-model.trim="new_password1" class="form-control">
      
      <label for="new_password2"><b>Confirm New Password : </b></label>
      <input type="password" id="new_password2" v-model.trim="new_password2" class="form-control">
      
      <label for="old_password"><b>Old Password : </b></label>
      <input type="password" id="old_password" v-model.trim="old_password" class="form-control">

      <input type="submit" value="비밀번호 변경" class="btn btn-primary">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps({
  selectedProfilePage: String
})

const router = useRouter()
const authStore = useAuthStore()

const new_password1 = ref(null)
const new_password2 = ref(null)
const old_password = ref(null)

const changePassword = function () {
  axios({
    method: 'post',
    url: `${authStore.API_URL}/accounts/password/change/`,
    data: {
      new_password1: new_password1.value,
      new_password2: new_password2.value,
      old_password: old_password.value,
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(res => {
      window.alert('비밀번호가 변경되었습니다.')
      new_password1.value = null
      new_password2.value = null
      old_password.value = null
      router.push({ name: 'ProfileView', params: { id: authStore.user.pk }})
    })
    .catch(err => {
        for(let i=0; Object.values(err.response.data).length > i; i++) {
          for(let j=0; Object.values(err.response.data)[i].length > j; j++) {
            alert(Object.values(err.response.data)[i][j])
          }
        }
      })
}
</script>

<style scoped>

</style>