<template>
  <div class="container">
    <div class="content">
      <b-table :data="[this.getData[0]]" :card-layout="true">
        <b-table-column
          field="id"
          label="ID"
          width="40"
          centered
          v-slot="props"
        >
          <p class="text-left">{{ props.row.id }}</p>
        </b-table-column>

        <b-table-column
          centered
          field="name"
          label="Scraper Name"
          v-slot="props"
        >
          <p class="text-left">{{ props.row.name }}</p>
        </b-table-column>

        <b-table-column field="url" label="URL" centered v-slot="props">
          <p class="text-center">{{ props.row.url }}</p>
        </b-table-column>

        <b-table-column field="status" label="Status" centered v-slot="props">
          <span
            class="tag"
            :class="{
              'is-success': props.row.status == 'finished',
              'is-warning': props.row.status == 'running',
            }"
          >
            <p class="text-left">{{ props.row.status }}</p>
          </span>
        </b-table-column>

        <b-table-column label="Results" centered v-slot="props">
          <div>
          <b-button
            @click="downloadResults"
            size="is-small"
            rounded
            outlined
            :type="{
              'is-warning': props.row.status == 'running',
              'is-success': props.row.status == 'finished',
            }"
          >
            results
          </b-button>
          <b-button @click="deleteScraper(props.row.id)" size="is-small" rounded outlined type="is-danger">
            DELETE
          </b-button>
          </div>
        </b-table-column>
      </b-table>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from 'axios'
export default {
  name: "OverviewOverlay",

  computed: {
    ...mapGetters(["getData"]),
  },

  methods: {
    deleteScraper(id) {
      const delete_request = 'https://bosa-inspector-widget.herokuapp.com/scrapers/' + String(id)
      console.log("this should delete the scraper")
      axios
      .delete(delete_request)
    },
    downloadResults(id) {
      const download_request = 'https://bosa-inspector-widget.herokuapp.com/scrapers/' + String(id) +'/export'
      console.log("this should download the results")
      axios
      .get(download_request)

    }
  }
  
};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 30px auto;
  overflow: auto;
  border: 5px solid #d43e25;
  border-radius: 5px;
  position: relative;
  top: 30px;
}

.content {
  padding: 50px;
  background-color: white;
}

.alignRight {
  text-align: right;
}
</style>
