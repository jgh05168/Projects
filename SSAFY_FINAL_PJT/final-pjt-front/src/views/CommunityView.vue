<template>
  <div>
    <div v-if="categorys" class="mx-3">
      <div v-for="category in categorys" :key="category.name" @click.prevent="selectedCategory(category)" class="d-inline-block me-3 mt-3">
        <p class="d-inline-block">
          <i v-if="category === selectedCategoryObj" class="bi bi-bookmark-fill"></i>
          <i v-else class="bi bi-bookmark"></i>
          {{ category.name }}
        </p>
        <!-- 카테고리 삭제 모달 -->
        <i class="bi bi-trash3-fill text-danger ms-1" v-if="authStore.user.is_superuser" data-bs-toggle="modal" :data-bs-target="'#category' + category.id"></i>
        <div class="modal fade" :id="'category' + category.id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">카테고리 삭제</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                선택한 카테고리를 삭제하시겠습니까 ?
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
                <button @click.prevent="categoryDelete(category.id)" class="btn btn-danger" data-bs-dismiss="modal">삭제</button>
              </div>
            </div>
          </div>
        </div>
        <!-- 카테고리 삭제 모달 -->
      </div>
      <Category
      :category="selectedCategoryObj"
      :appViewHeight="appViewHeight"
      class="mt-3"/>
    </div>
  </div>
</template>

<script setup>
import Category from '@/components/Category.vue'
import { ref, onMounted } from 'vue'
import { usePostStore } from '@/stores/post'
import { useAuthStore } from '../stores/auth';
import axios from 'axios'

const props = defineProps({
  appViewHeight: Number
})

const postStore = usePostStore()
const authStore = useAuthStore()
const selectedCategoryObj = ref(null)
const categorys = ref(null)

const selectedCategory = (category) => {
  postStore.selectedCategory = category
  selectedCategoryObj.value = category
  postStore.getPosts(category.id)
}

const categoryDelete = (categoryId) => {
  axios({
    method: 'delete',
    url: `${postStore.API_URL}/api/v1/category/${categoryId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
    .then((res) => {
      const itemIdx = postStore.category.findIndex((item) => item.id === categoryId)
      postStore.category.splice(itemIdx, 1)
      categorys.value = postStore.category
      selectedCategoryObj.value = null
      postStore.selectedCategory = null
      postStore.getPosts()
    })
    .catch((err) => {
      console.log(err)
    }) 
}

onMounted(() => {
  postStore.getCategory()
  categorys.value = postStore.category
  postStore.getPosts()
  selectedCategoryObj.value = postStore.selectedCategory
})
</script>

<style scoped>

</style>