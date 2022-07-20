<template>
    <div class="container">
    <b-table :data="[this.getData[0]]">
      <b-table-column   field="id" label="ID" width="40" centered v-slot="props">
        <p class="text-left" > {{ props.row.id }} </p>
      </b-table-column>

      <b-table-column centered field="name" label="Scraper Name" v-slot="props">
        <p class="text-left" > {{ props.row.name }} </p>
      </b-table-column>

      <b-table-column field="url" label="URL" centered v-slot="props">
        <p class="text-center" > {{ props.row.url }} </p>
      </b-table-column>


      <b-table-column field="status" label="Status" centered v-slot="props">
        <span
          class="tag"
          :class="{
            'is-success': props.row.status == 'finished',
            'is-warning': props.row.status == 'running',
          }"
        >
          <p class="text-left" >{{ props.row.status }} </p>
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
    </b-table>
    </div>
</template>


<script>
import {mapGetters} from 'vuex'
export default {
    name: 'OverviewOverlay',

    computed: {
        ...mapGetters(['getData'])
    }
    // props: {
    //     url: String,
    //     start_date: String,
    //     end_date: String,
    // }
}
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 30px auto;
  overflow: auto;
  min-height: 300px;
  border: 5px solid #D43E25;
  padding: 30px;
  border-radius: 5px;
  position: relative;
  top: 30px;
}
</style>


