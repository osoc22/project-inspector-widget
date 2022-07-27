<template>
  <b-field label="Insert Scraper Name">
    <b-input @input="saveName" />
  </b-field>
</template>

<script>
import {mapMutations} from 'vuex'
export default {
  name: "InsertName",

  methods: {
    ...mapMutations(['SET_NAME']),
    saveName(n) {
      this.SET_NAME(n)
    },
  },
};
</script>

<style scoped>
.input {
  margin: auto;
  width: 100%;
  padding: 50px;
}
</style>
