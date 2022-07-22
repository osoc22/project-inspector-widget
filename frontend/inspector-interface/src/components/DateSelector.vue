<template>
  <div >
    <b-field label="Select a period">
      <b-datepicker
        v-model="start_date"
        placeholder="Select start date"
      />
      <b-datepicker
        v-model="end_date"
        placeholder="Select end date"

      />
    </b-field>
  </div>
</template>

<script>
import { mapMutations }  from 'vuex'

export default {
  name: "DateSelector",

  data() {
    return {
      start_date: null,
      end_date: null
    }
  },

  methods: {
    ...mapMutations(['SET_START_DATE','SET_END_DATE' ]),
    
    checkTime(i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    },
    time() {
      var date = new Date();
      var hh = date.getHours();
      var mm = date.getMinutes();
      var ss = date.getSeconds();
  
      // adding 0 for single digits
      
      mm = this.checkTime(mm);
      ss = this.checkTime(ss);
      return hh + ":" + mm + ":" + ss;
    },
    formatDate(date) {
      let formatted_date = date.getFullYear() +
          "-" +
          ("0" + (date.getMonth() + 1)).slice(-2) +
          "-" +
          ("0" + date.getDate()).slice(-2) +
          " " +
          this.time();
        return formatted_date
    },
  
  },
  watch: {
    start_date(val) {
      this.SET_START_DATE(this.formatDate(val))
    },
    end_date(val) {
      this.SET_END_DATE(this.formatDate(val))
    }
  }
};
</script>

<style scoped>
.input {
  margin: 10px auto;
  width: 100%;
  padding: 50px;
}


</style>
