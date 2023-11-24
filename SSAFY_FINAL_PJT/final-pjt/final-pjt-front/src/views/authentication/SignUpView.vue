<template>
  <div class="mx-3">
    <AuthForm :name="route.name"/>
  </div>
</template>

<script setup>
import AuthForm from '@/components/AuthForm.vue';
import { useRoute } from 'vue-router';

const route = useRoute()

</script>

<style scoped>

</style>