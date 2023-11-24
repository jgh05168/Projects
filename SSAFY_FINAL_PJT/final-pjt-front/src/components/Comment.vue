<template>
  <div>
    <CommentCreate :post="post" @comment-create="commentCreate"/>
    <hr>
    
    <div v-for="comment in postStore.comments" :key="comment.id">
      <p>
        <span v-if="post.category.name !== '익명게시판'" :class="{'text-secondary': isMyComment(comment) }">{{ comment.user.username }} 님의 댓글 : {{ comment.content }}</span>
        <span v-else :class="{'text-secondary': isMyComment(comment) }">익명{{ comment.user.pk }} 님의 댓글 : {{ comment.content }}</span>
        <i v-if="authStore.user.pk === comment.user.pk"
          @click.prevent="commentDelete(comment.id)" class="bi bi-x-square text-danger ms-2">
        </i>
      </p>
    </div>
  </div>
</template>

<script setup>
import CommentCreate from '@/components/CommentCreate.vue'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usePostStore } from '@/stores/post'
import axios from 'axios'

const props = defineProps({
  post: Object
})

const authStore = useAuthStore()
const postStore = usePostStore()

const commentCreate = (newComment) => {
  postStore.comments.push(newComment)
}

const commentDelete = (commentId) => {
  axios({
    method: 'delete',
    url: `${postStore.API_URL}/api/v1/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      postStore.getComments(props.post.id)
    })
    .catch((err) => {
      console.log(err)
    })
}

const isMyComment = computed (() => {
  return (comment) => authStore.user.pk !== comment.user.pk
})
</script>

<style scoped>

</style>