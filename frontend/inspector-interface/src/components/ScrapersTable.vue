<template>
  <section>
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

      <b-table-column>
        <button class="plain" @click="showOverview">
          <mdicon name="information-outline" />
        </button>
      </b-table-column>
    </b-table>
    <b-modal
      v-model="this.getOverview"
      title="Scraper Information"
      :can-cancel="true"
      trap-focus
    >
      <overview-overlay />
    </b-modal>
  </section>
</template>

<script>
import axios from "axios";
import { mapGetters, mapMutations } from "vuex";
import OverviewOverlay from "./OverviewOverlay.vue";

export default {
  name: "ScrapersTable",
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
    showOverview() {
      console.log("this should start the scraper");
      this.SET_OVERVIEW(true);
    },
  },
  created() {
    console.log(this.getAccessToken)
    axios
            .get('https://bosa-inspector-widget.herokuapp.com/scrapers/user', {
                headers: {
                    Authorization: `Bearer ${this.getAccessToken}`
                }
            })
            .then(result => this.SET_DATA(result.data))
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
