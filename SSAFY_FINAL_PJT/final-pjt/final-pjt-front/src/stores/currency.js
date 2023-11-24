import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

export const useCurrencyRateStore = defineStore('currency', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const authStore = useAuthStore()
  const exchange_db = ref(null)


  const getExchangeRate = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/exchange_rates/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        // console.log(res.data)
        exchange_db.value = res.data
      })
      .catch(err => console.log(err))
  }


  return {getExchangeRate, exchange_db}
})