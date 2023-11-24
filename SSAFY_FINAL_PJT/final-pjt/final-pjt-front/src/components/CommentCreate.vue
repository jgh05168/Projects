<template>
  <div>
    <form @submit.prevent="commentCreate" class="d-flex align-items-center">
      <label for="comment" class="col-form-label">내용 : </label>
      <input type="text" id="comment" class="form-control flex-grow-1 mx-3" v-model="content">
      <input type="submit" value="댓글 작성" class="btn btn-outline-secondary border-secondary">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps({
  post: Object
})

const emit = defineEmits(['commentCreate'])

const postStore = usePostStore()
const authStore = useAuthStore()
const content = ref(null)

const commentCreate = function () {
  axios({
    method: 'post',
    url: `${postStore.API_URL}/api/v1/posts/${props.post.id}/comments/`,
    data: {
      content: content.value
    },
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  }).then((res) => {
    content.value = ''
    const newComment = res.data
    emit('commentCreate', newComment)
  }).catch(err => console.log(err))
}
</script>

<style scoped>
#comment {
  width: 50%;
}
</style>