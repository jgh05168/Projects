<template>
  <div class="container my-3">
    <div v-if="currencyStore.exchange_db" class="d-flex flex-column align-items-center justify-content-center" style="height: 100%;">
      <h2><i class="bi bi-cash-coin text-secondary"></i> 환율 계산기</h2>
      <h4>- 국가 별 매매기준율 -</h4>
    <div class="row container mt-2 mb-4">
      <div class="col-sm-4 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">미국(USA)</h5>
            <p>{{ getCountry('USD').cur_nm }} : USD {{ getCountry('USD').deal_bas_r }} </p>
          </div>
        </div>
      </div>
      <div class="col-sm-4 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">일본(Japan)</h5>
            <p>{{ getCountry('JPY(100)').cur_nm }} : JPY {{ getCountry('JPY(100)').deal_bas_r }} </p>
          </div>
        </div>
      </div>
      <div class="col-sm-4 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">유럽 연합(EU)</h5>
            <p>{{ getCountry('EUR').cur_nm }} : EUR {{ getCountry('EUR').deal_bas_r }}</p>
          </div>
        </div>
      </div>
      <div class="mb-3">

      </div>
      <div class="col-sm-4 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">영국(UK)</h5>
            <p>{{ getCountry('GBP').cur_nm }} : GBP {{ getCountry('GBP').deal_bas_r }}</p>
          </div>
        </div>
      </div>
      <div class="col-sm-4 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">중국(China)</h5>
            <p>{{ getCountry('CNH').cur_nm }} : CNH {{ getCountry('CNH').deal_bas_r }}</p>
          </div>
        </div>
      </div>
      <div class="col-sm-4 mb-3 mb-sm-0">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">스위스 연방(CH)</h5>
            <p>{{ getCountry('CHF').cur_nm }} : CHF {{ getCountry('CHF').deal_bas_r }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="container row">
      <h3>원화 ➔ 외화</h3>
      <div class="d-flex justify-content-between">
        <select style="width: 60%;" class="form-select" aria-label="Default select example" v-model="selectWonCountry" @change.prevent="setSelect()">
          <option v-for="curCountry in currencyStore.exchange_db" :key="currencyStore.exchange_db.ttb">{{ curCountry.cur_nm }}</option>
        </select>
        <input style="width: 30%;" class="input" type="text" v-model="befWonValue">
        
      </div>
      <div class="input-group my-3">
        <span class="input-group-text" id="inputGroup-sizing-default">Change</span>
        <div class="form-control d-flex justify-content-center" v-if="claculateWonValue">{{claculateWonValue}}</div>
      </div>
      
      <h3>외화 ➔ 원화</h3>
      <div class="d-flex justify-content-between">
        <select style="width: 60%;" class="form-select" aria-label="Default select example" v-model="selectOtherCountry"  @change.prevent="setSelect()">
          <option v-for="curCountry in currencyStore.exchange_db" :key="currencyStore.exchange_db.tts">{{ curCountry.cur_nm }}</option>
        </select>
        <input style="width: 30%;" class="input" type="text" v-model="befOtherValue">
      </div>
      <div class="input-group my-3">
        <span class="input-group-text" id="inputGroup-sizing-default">Change</span>
        <div class="form-control d-flex justify-content-center" v-if="claculateOtherValue">{{claculateOtherValue}}</div>
      </div>
    </div>
  </div>
    
    <div v-else>
      <p>로딩중 ..</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCurrencyRateStore } from '@/stores/currency'
import { computed } from '@vue/reactivity'

const currencyStore = useCurrencyRateStore()
const befWonAmount = ref(null)
const befOtherAmount = ref(null)
const selectWonCountry = ref(null)
const selectOtherCountry = ref(null)
const befWonValue = ref(null)
const befOtherValue = ref(null)

const getCountry = function (code) {
  return currencyStore.exchange_db.find(item => item.cur_unit === code)
}


const setSelect = function () {
  currencyStore.exchange_db.forEach((key) => {
    if (selectWonCountry.value === key.cur_nm) {
      if (selectWonCountry.value === '일본 옌' || selectWonCountry.value === '인도네시아 루피아') {
        befWonAmount.value = key.ttb.replace(',', '') / 100
      } else {
        befWonAmount.value = key.ttb.replace(',', '')
      }
    }
    if (selectOtherCountry.value === key.cur_nm) {
      if (selectOtherCountry.value === '일본 옌' || selectOtherCountry.value === '인도네시아 루피아') {
        befOtherAmount.value = key.tts.replace(',', '') / 100
      } else {
        befOtherAmount.value = key.tts.replace(',', '')
      }
    }
  })

}


const claculateWonValue = computed(() => {
    return (befWonValue.value / befWonAmount.value).toFixed(2)
})

const claculateOtherValue = computed(() => {
    return (befOtherValue.value * befOtherAmount.value).toFixed(2)
})

onMounted (() => {
  currencyStore.getExchangeRate()
})

</script>

<style scoped>
.card {
  width: 100%;
  height: 100%;
}
</style>