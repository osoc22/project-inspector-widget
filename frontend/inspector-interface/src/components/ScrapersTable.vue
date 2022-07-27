<template>
  <div>
    <b-table :data="this.getData">
      <b-table-column field="id" label="ID" width="40" centered v-slot="props">
        <p class="text-left">{{ props.row.id }}</p>
      </b-table-column>

      <b-table-column centered field="name" label="Scraper Name" v-slot="props">
        <p class="text-left">{{ props.row.name }}</p>
      </b-table-column>

      <!-- <b-table-column field="url" label="URL" centered v-slot="props">
        <p class="text-center" > {{ props.row.url }} </p>
      </b-table-column> -->

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
      </b-table-column>

      <b-table-column v-slot="props">
        <button class="plain" @click="() => showOverview(props.row)">
          <mdicon name="information-outline" />
        </button>
      </b-table-column>
    </b-table>
    <b-modal
      v-model="show_overview"
      title="Scraper Information"
      has-modal-card
      trap-focus
      :destroy-on-hide="false"
      :on-cancel="closeOverview"
    >
      <overview-overlay :scraper_data="selected_scraper" />
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters, mapMutations } from "vuex";
import OverviewOverlay from "./OverviewOverlay.vue";

export default {
  name: "ScrapersTable",

  data() {
    return {
      show_overview: false,
      selected_scraper: null
    }
  },
  components: {
    OverviewOverlay,
  },

  computed: {
    ...mapGetters(["getData", "getOverview", "getAccessToken"]),
  },

  methods: {
    ...mapMutations(["SET_DATA", "SET_OVERVIEW"]),

    downloadResults() {
      console.log("this should download the results");
    },
    showOverview(input) {
      console.log(input)
      this.selected_scraper = input
      this.show_overview = true
    },
    closeOverview() {
      this.show_overview = false
      this.selected_scraper = null
    }
  },
  created() {
    console.log(this.getAccessToken);
    axios
      .get("https://bosa-inspector-widget.herokuapp.com/scrapers/user", {
        headers: {
          Authorization: `Bearer ${this.getAccessToken}`,
        },
      })
      .then((result) => this.SET_DATA(result.data));
  },
};
</script>

<style scoped>
.text_center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.plain {
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
  outline: inherit;
}
</style>
