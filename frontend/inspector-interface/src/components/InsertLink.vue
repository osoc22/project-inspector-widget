<template>
  <b-field label="Insert Link">
    <b-input @blur="saveLink" />
  </b-field>
</template>

<script>
import {mapMutations} from 'vuex'
export default {
  name: "InsertLink",

  methods: {
    ...mapMutations(['SET_URL']),
    saveLink(l) {
      this.SET_URL(l)
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
