<template>
<div>

    <div class="container">
        <insert-name />
        <insert-link />
        <div class="aboveSpacing">
            <date-selector />
        </div>
        <div class="aboveSpacing">
            <b-button
                type="is-danger"
                class="btn"
                :rounded="true"
                size="is-medium"
                @click="startScraper">
            START SCAN </b-button>
        </div>
    </div>
    <div class="container">
        <scrapers-table />
    </div>
</div>
</template>


<script>
import InsertLink from '@/components/InsertLink.vue'
import ScrapersTable from '@/components/ScrapersTable.vue'
import DateSelector from '@/components/DateSelector.vue'
import InsertName from '../components/InsertName.vue'
import {mapGetters, mapMutations} from 'vuex'
import axios from 'axios'
export default {
    name: 'ScraperDashboard',
    components: {
        ScrapersTable,
        InsertLink,
        DateSelector,
        InsertName
    },
    computed: {
        ...mapGetters(['getStartDate','getEndDate','getURL', 'getName'])
    },
    
    methods: {
        ...mapMutations(['SET_DATA']),
        startScraper() {
            axios
            .post('https://bosa-inspector-widget.herokuapp.com/scrapers', {
                "name": this.getName,
                "start_date": this.getStartDate,
                "end_date": this.getEndDate,
                "url": this.getURL,
                "status": "running"
            })
            .then(console.log("scraper has been added"))

            axios
            .get('https://bosa-inspector-widget.herokuapp.com/scrapers')
            .then(result => this.SET_DATA(result.data))
          
        },
    },
   

    
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

.aboveSpacing {
    margin: auto;
    position: relative;
    top: 10px;
    padding: 10px;
    
}
</style>


