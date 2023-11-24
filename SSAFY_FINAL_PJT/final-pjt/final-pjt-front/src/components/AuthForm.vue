<template>
  <div class="container mt-5">
    <h2 v-if="name === 'SignUpView'"><b>회원가입 페이지</b></h2>
    <h2 v-else-if="name === 'LogInView'"><b>로그인 페이지</b></h2>
    <div class="form-control">
      <form @submit.prevent="submitInfo" class="d-flex flex-column p-3 gap-2">
        <label for="username"><b>Username : </b></label>
        <input type="text" id="username" v-model.trim="username" class="form-control"><br>
        
        <label for="password1"><b>Password : </b></label>
        <input type="password" id="password1" v-model.trim="password1" class="form-control"><br>
        
        <div v-if="name === 'SignUpView'">
          <label for="password2"><b>Confirm Password : </b></label>
          <input type="password" id="password2" v-model.trim="password2" class="form-control">
        </div>
        
        <input v-if="name === 'SignUpView'" type="submit" value="회원 가입" class="btn btn-primary">
        <input v-else-if="name === 'LogInView'" type="submit" value="로그인" class="btn btn-primary">
      </form>
      <RouterLink v-if="name === 'LogInView'" :to="{ name: 'SignUpView' }" class="d-flex flex-column btn btn-primary mx-3" >회원가입</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  name: String
})

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const authStore = useAuthStore()

const submitInfo = function () {
  const payload = {
    username: username.value,
    password: password1.value,
    password1: password1.value,
    password2: password2.value
  }
  if (props.name === 'SignUpView')
    authStore.signUp(payload)
  else if ((props.name === 'LogInView'))
    authStore.logIn(payload)
}
</script>

<style scoped>
/* form {
  width: 30%;
  margin: 0 auto;
} */
</style>