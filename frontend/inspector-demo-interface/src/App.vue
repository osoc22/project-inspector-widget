<template>
  <div id="app" class="container">
    <h1 class="title">First DEMO 18/07/2022</h1>
    <InsertLink @getLink="saveLink" />
    <b-button
      type="is-info"
      class="btn"
      :rounded="true"
      size="is-medium"
      @click="displayLink"
    >
      START SCAN
    </b-button>
    <p>test</p>
    <b-table :data="data" :colums="columns" />
    <p>test 2</p>
  </div>
</template>

<script>
import InsertLink from "./components/InsertLink.vue";

export default {
  name: "App",
  components: {
    InsertLink,
  },

  data() {
    return {
      link: "",
      data: [
        {
          id: 1,
          first_name: "Jesse",
          last_name: "Simmons",
          date: "2016-10-15 13:43:27",
          gender: "Male",
        },
        {
          id: 2,
          first_name: "John",
          last_name: "Jacobs",
          date: "2016-12-15 06:00:53",
          gender: "Male",
        },
        {
          id: 3,
          first_name: "Tina",
          last_name: "Gilbert",
          date: "2016-04-26 06:26:28",
          gender: "Female",
        },
        {
          id: 4,
          first_name: "Clarence",
          last_name: "Flores",
          date: "2016-04-10 10:28:46",
          gender: "Male",
        },
        {
          id: 5,
          first_name: "Anne",
          last_name: "Lee",
          date: "2016-12-06 14:38:38",
          gender: "Female",
        },
      ],
      columns: [
        {
          field: "id",
          label: "ID",
          width: "40",
          numeric: true,
        },
        {
          field: "first_name",
          label: "First Name",
        },
        {
          field: "last_name",
          label: "Last Name",
        },
        {
          field: "date",
          label: "Date",
          centered: true,
        },
        {
          field: "gender",
          label: "Gender",
        },
      ],
    };
  },
  mounted() {
    console.log({ data: this.data, columns: this.columns });
  },
  methods: {
    displayLink() {},

    saveLink(l) {
      this.link = l;
    },
  },
};
</script>

<style>
.container {
  max-width: 500px;
  margin: 30px auto;
  overflow: auto;
  min-height: 300px;
  border: 5px solid #307df0;
  padding: 30px;
  border-radius: 5px;
  position: relative;
  top: 30px;
}

.btn {
  display: inline-block;
  background: #000;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  font-size: 15px;
  font-family: inherit;
  width: 100%;
}

.title {
  font-weight: bold;
}
</style>
