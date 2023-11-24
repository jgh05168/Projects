<template>
  <div>
    <!-- 회원탈퇴 모달 -->
    <button class="btn btn-info btn-sm ms-2 text-light" data-bs-toggle="modal" :data-bs-target="'#user' + fieldName">
      수정하기
    </button>
    <div class="modal fade" :id="'user' + fieldName" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">회원정보 수정</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateField">
              <p>{{ field }} 정보를 수정합니다.</p>
              <input type="text" class="form-control mb-3" v-model="fieldValue">
              <div class="text-end">
                <button class="btn btn-secondary me-2" data-bs-dismiss="modal">취소</button>
                <button type='submit' class="btn btn-danger" data-bs-dismiss="modal">확인</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- 회원탈퇴 모달 -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios';

const props = defineProps({
  fieldName: String
})

const emit = defineEmits(['updateProfile'])

const authStore = useAuthStore()
const fieldValue = ref('')
const field = ref('')

const updateField = function () {
  axios({
    method: 'post',
    url: `${authStore.API_URL}/accounts/profile/update/${authStore.user.pk}/`,
    data: {
      username: authStore.user.username,
      [props.fieldName]: fieldValue.value
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then(res => {
      console.log(`${props.fieldName}(이)가 수정되었습니다.`)
      authStore.user = { ...authStore.user, [props.fieldName]: res.data[props.fieldName] }
      emit('updateProfile')
    })
    .catch(err => {
      for(let i=0; Object.values(err.response.data).length > i; i++) {
        for(let j=0; Object.values(err.response.data)[i].length > j; j++) {
          alert(Object.values(err.response.data)[i][j])
        }
      }
    })
}

onMounted(() => {
  if (props.fieldName === 'age') {
    fieldValue.value = authStore.user.age
    field.value = '나이'
  } else if ( props.fieldName === 'nickname') {
    fieldValue.value = authStore.user.nickname
    field.value = '닉네임'
  } else if ( props.fieldName === 'email') {
    fieldValue.value = authStore.user.email
    field.value = '이메일'
  } else if ( props.fieldName === 'money') {
    fieldValue.value = authStore.user.money
    field.value = '보유 자산'
  } else if ( props.fieldName === 'salary') {
    fieldValue.value = authStore.user.salary
    field.value = '연봉'
  }
})
</script>

<style scoped>

</style>