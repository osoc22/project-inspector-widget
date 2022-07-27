<template>
  <div class="container" v-if="scraper_data">
    <div class="content">
      <b-table :data="[selected_scraper]" :card-layout="true">
        <b-table-column
          field="id"
          label="ID"
          width="40"
          centered
        >
          <p class="text-left">{{ scraper_data.id }}</p>
        </b-table-column>

        <b-table-column
          centered
          field="name"
          label="Scraper Name"
        >
          <p class="text-left">{{ scraper_data.name }}</p>
        </b-table-column>

        <b-table-column field="url" label="URL" centered >
          <p class="text-center">{{ scraper_data.url }}</p>
        </b-table-column>

        <b-table-column field="status" label="Status" centered >
          <span
            class="tag"
            :class="{
              'is-success': scraper_data.status.toUpperCase() == 'FINISHED',
              'is-warning': scraper_data.status.toUpperCase() == 'RUNNING',
            }"
          >
        
            <p class="text-left">{{ scraper_data.status }}</p>
          </span>
        </b-table-column>

        <b-table-column label="Results" centered>
          <div>
            <b-button
              @click="downloadResults"
              size="is-small"
              rounded
              outlined
              :type="{
                'is-warning': scraper_data.status == 'running',
                'is-success': scraper_data.status == 'finished',
              }"
            >
              results
            </b-button>
            <b-button
              @click="() => deleteScraper(scraper_data.id)"
              size="is-small"
              rounded
              outlined
              type="is-danger"
            >
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
import axios from "axios";
export default {
  name: "OverviewOverlay",

  computed: {
    ...mapGetters(["getData", "getAccessToken"]),
  },
  props: {
    scraper_data: {
      type: Object,
      default: null,
      required: true,
    },
  },
  mounted() {
    console.log(this.scraper_data)
  },

  methods: {
    deleteScraper(id) {
      const delete_request =
        "https://bosa-inspector-widget.herokuapp.com/scrapers/" + String(id);
      console.log("this should delete the scraper");
      axios.delete(delete_request, {
        headers: {
          Authorization: `Bearer ${this.getAccessToken}`,
        },
      });
    },
    downloadResults(id) {
      const download_request =
        "https://bosa-inspector-widget.herokuapp.com/scrapers/" +
        String(id) +
        "/export";
      console.log("this should download the results");
      axios
        .get(download_request, {
          headers: {
            Authorization: `Bearer ${this.getAccessToken}`,
          },
        })
        .then(console.log("file was downloaded"));
    },
   
  },

};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 30px auto;
  overflow: auto;
  border: 5px solid #2782c6;
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
