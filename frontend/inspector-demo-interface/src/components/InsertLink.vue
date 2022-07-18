<template>
  <b-field label="Insert Link">
    <b-input @blur="saveLink" />
  </b-field>
</template>

<script>
export default {
  name: "InsertLink",

  data() {
    return {
      link: "",
    };
  },

  methods: {
    saveLink(l) {
      this.link = l.target.value;
      this.$emit("getLink", this.link);
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
