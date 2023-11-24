import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usePostStore } from '@/stores/post'
import MainView from '../views/MainView.vue'
import ProfileView from '../views/ProfileView.vue'
import ProductCompareView from '../views/ProductCompareView.vue'
import CurrencyCalculationView from '../views/CurrencyCalculationView.vue'
import BankNearbyView from '../views/BankNearbyView.vue'
import CommunityView from '../views/CommunityView.vue'
import CategoryCreateView from '../views/crud/CategoryCreateView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'

import SignUpView from '../views/authentication/SignUpView.vue'
import LogInView from '../views/authentication/LogInView.vue'

import PostCreateView from '../views/crud/PostCreateView.vue'
import PostUpdateView from '../views/crud/PostUpdateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView
    },
    {
      path: '/profile/:id',
      name: 'ProfileView',
      component: ProfileView
    },
    {
      path: '/product',
      name: 'ProductCompareView',
      component: ProductCompareView
    },
    {
      path: '/currency',
      name: 'CurrencyCalculationView',
      component: CurrencyCalculationView
    },
    {
      path: '/bank',
      name: 'BankNearbyView',
      component: BankNearbyView
    },
    {
      path: '/comunnity',
      name: 'CommunityView',
      component: CommunityView
    },
    {
      path: '/detail/:id',
      name: 'PostDetailView',
      component: PostDetailView
    },
    {
      path: '/product/detail/:name',
      name: 'ProductDetailView',
      component: ProductDetailView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/category',
      name: 'CategoryCreateView',
      component: CategoryCreateView,
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (!authStore.user.is_superuser) {
          console.log('관리자가 아닙니다.')
          return { name: from.name }
        } else {
          next()
        }
      }
    },
    {
      path: '/post/create/:categoryId',
      name: 'PostCreateView',
      component: PostCreateView
    },
    {
      path: '/post/:id',
      name: 'PostUpdateView',
      component: PostUpdateView
    },
  ]
})

router.beforeEach((to, from) => {
  const authStore = useAuthStore()
  const postStore = usePostStore()
  if (to.name !== 'PostDetailView' && to.name !== 'CommunityView' && to.name !== 'PostCreateView' && to.name !== 'PostUpdateView'){
    postStore.selectedCategory = null
  }
  if (to.name !== 'MainView' && to.name !== 'SignUpView' && to.name !== 'LogInView' && !authStore.isAuthenticated) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView'}
  }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (authStore.isAuthenticated)) {
    window.alert('이미 로그인이 되어있습니다.')
    return { name: 'MainView' }
  }

  if (to.name !== 'ProfileView' && to.name !== 'ProductDetailView' && to.name !== 'ProductCompareView') {
    authStore.selectedProfilePage = '기본 정보 수정'
  }
})
export default router
