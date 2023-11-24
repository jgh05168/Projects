import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const authStore = useAuthStore()
  const banks = ref([])
  const deposit_product = ref([])
  const deposit_option = ref([])
  const saving_product = ref([])
  const saving_option = ref([])
  const all_products = ref([])
  // 상품 추천 데이터
  const recommand_list = ref(null)
  const rec_per_money = ref(null)
  const rec_per_age = ref(null)
  const rec_per_salary = ref(null)
  
  const getBanks = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/data_load/bank/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        banks.value = res.data
      })
      .catch(err => console.log(err))
  }

  const getDepositProduct = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/data_load/depositproduct/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        deposit_product.value = res.data
      })
      .catch(err => console.log(err))
  }

  const getDepositOption = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/data_load/deposit/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        deposit_option.value = res.data
      })
      .catch(err => console.log(err))
  }

  const getSavingProduct = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/data_load/savingproduct/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        const uniqueSavingProducts = Array.from(new Set(res.data.map(item => item.fin_prdt_nm))).map(fin_prdt_nm => res.data.find(item => item.fin_prdt_nm === fin_prdt_nm));
        saving_product.value = uniqueSavingProducts
      })
      .catch(err => console.log(err))
  }

  const getSavingOption = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/data_load/saving/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(res => {
        saving_option.value = res.data
      })
      .catch(err => console.log(err))
  }

  const total_products = function () {
    all_products.value = deposit_product.value.concat(saving_product.value)
  }


  // 상품 추천 받기
  const recommendProducts = function () {
    function compareAge(a, b) {
      return Math.abs(a.age - authStore.user.age) - Math.abs(b.age - authStore.user.age);
    }
    function compareMoney(a, b) {
      return Math.abs(a.money - authStore.user.money) - Math.abs(b.money - authStore.user.money);
    }
    function compareSalary(a, b) {
      return Math.abs(a.salary - authStore.user.salary) - Math.abs(b.salary - authStore.user.salary);
    }
    
    rec_per_age.value = authStore.userList.slice().sort(compareAge)
    rec_per_money.value = authStore.userList.slice().sort(compareMoney)
    rec_per_salary.value = authStore.userList.slice().sort(compareSalary)

    let productInfo = null
    const kor_nm = ref('')
    const getProductName = function (prdt_cd) {
      productInfo = all_products.value.filter(item => item.fin_prdt_cd === prdt_cd)

      if (Array.isArray(productInfo) && productInfo.length > 0) {
        kor_nm.value = productInfo[0].fin_prdt_nm
        return true
      } else {
        kor_nm.value = ''
        return false
      }
    }

    let temp_product_list = []
    let score = 0
    let isSave = false
    let has_kor_nm = false

    rec_per_age.value.forEach((obj) => {
      isSave = false
      if (obj.financial_products != null) {
        obj.financial_products.split(',').forEach(index => {
          // console.log(index)
          if (!temp_product_list.find(item => item.products === index) && index != '') {
            has_kor_nm = getProductName(index)
            if (has_kor_nm) {
              temp_product_list.push({score: score, products: index, cnt: 1, kor_nm: kor_nm.value})
              isSave = true
            }
          } 
        })
        if (isSave) {
          score++;
        }
      }
    })


    // 초기에는 안쌓아주고 바로 저장
    recommand_list.value = temp_product_list

    // money
    temp_product_list = []
    score = 0
    rec_per_money.value.forEach((obj) => {
      isSave = false
      if (obj.financial_products != null) {
        obj.financial_products.split(',').forEach(index => {
          // console.log(index)
          if (!temp_product_list.find(item => item.products === index)) {
            has_kor_nm = getProductName(index)
            if (has_kor_nm) {
              temp_product_list.push({score: score, products: index, cnt: 1, kor_nm: kor_nm.value})
              isSave = true
            }
          } 
        })
        if (isSave) {
          score++;
        }
      }
    })

    let idx = 0
    temp_product_list.forEach(obj => {
      if (recommand_list.value.find((item, index) => {
        idx = index
        return item.products === obj.products
      })) {
        recommand_list.value[idx].score += obj.score
        recommand_list.value[idx].cnt++
      } else if (recommand_list.value.find(item => !item.products === '')) {
        recommand_list.value.push(obj)
      }
    })

    // salary
    temp_product_list = []
    score = 0
    rec_per_salary.value.forEach((obj) => {
      isSave = false
      if (obj.financial_products != null) {
        obj.financial_products.split(',').forEach(index => {
          // console.log(index)
          if (!temp_product_list.find(item => item.products === index)) {
            has_kor_nm = getProductName(index)
            if (has_kor_nm) {
              temp_product_list.push({score: score, products: index, cnt: 1, kor_nm: kor_nm.value})
              isSave = true
            }
          } 
        })
        if (isSave) {
          score++;
        }
      }
    })

    temp_product_list.forEach(obj => {
      if (recommand_list.value.find((item, index) => {
        idx = index
        return item.products === obj.products
      })) {
        recommand_list.value[idx].score += obj.score
        recommand_list.value[idx].cnt++
      } else if (recommand_list.value.find(item => !item.products === ''))  {
        recommand_list.value.push(obj)
      }
    })

    // cnt 내림차순 & score 오름차순으로 정렬
    recommand_list.value.sort((a, b) => {
      // 먼저 cnt를 기준으로 정렬
      if (a.cnt !== b.cnt) {
        return b.cnt - a.cnt; // cnt가 높은 순서대로
      } else {
        // cnt가 동일한 경우 score를 기준으로 정렬
        return a.score - b.score; // score가 낮은 순서대로
      }
    })
    // console.log(recommand_list.value)
  }

  return { banks, all_products, deposit_product, deposit_option, saving_product, saving_option, recommand_list,
    getBanks, getDepositProduct, getDepositOption, getSavingProduct, getSavingOption, recommendProducts, total_products,
  }
}, { persist: true })
