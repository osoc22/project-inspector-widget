<template>
  <div id="app" class="container">
    <h1 class="title">First DEMO 18/07/2022</h1>
    <InsertLink @getLink="saveLink" />
    <b-button
      type="is-info"
      class="btn"
      :rounded="true"
      size="is-medium"
      @click="startScraper"
    >
      START SCAN
    </b-button>
    <b-table :data="data" :columns="columns" />
  </div>
</template>

<script>
import InsertLink from "./components/InsertLink.vue";
import axios from 'axios'

export default {
  name: "App",
  components: {
    InsertLink,
  },

  data() {
    return {
      link: "",
      data: [],
      columns: [
        {
          field:'id',
          label: 'ID'
        },
        {
          field:'name',
          label: 'Name'
        },
        {
          field:'article_number',
          label: 'Article Number'
        },
        {
          field:'price_current',
          label: 'Current Price'
        },
        {
          field:'price_reference',
          label: 'Reference Price'
        },
        {
          field:'screenshot',
          label: 'Screenshot'
        },
        {
          field:'webshop',
          label: 'Webshop'
        },
        {
          field:'date',
          label: 'Date'
        },

      ]
    };
  },

  methods: {
    startScraper() {
      console.log(this.link)
      axios.post("http://127.0.0.1:8500/start-scraper", {
        "url": this.link
      })
      .then(response => console.log("it worked"))

      // axios
      //     .get('http://127.0.0.1:8500/products')
      //     .then(response => (this.data = response.data)) 
    },

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
