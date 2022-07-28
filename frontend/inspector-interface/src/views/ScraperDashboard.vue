<template>
    <div class="scraper-dashboard">
        <b-field label="Insert Scraper Name" class="wider">
            <b-input class="input_field" v-model="name" />
        </b-field>
        <b-field label="Insert Link" class="wider">
            <b-input class="input_field" v-model="url" />
        </b-field>
        <div class="aboveSpacing">
            <div>
                <b-field label="Select a period">
                    <b-datepicker
                        v-model="start_date"
                        placeholder="Select start date"
                        class="halfWidth input_field"
                    />
                    <b-datepicker
                        v-model="end_date"
                        placeholder="Select end date"
                        class="halfWidth input_field"
                    />
                </b-field>
            </div>
        </div>
        <div class="aboveSpacing">
            <b-button
                class="btn test"
                :rounded="true"
                size="is-medium"
                @click="startScraper"
            >
                START SCAN
            </b-button>
        </div>
        <div class="container">
            <scrapers-table />
        </div>
    </div>
</template>

<script>
import ScrapersTable from '@/components/ScrapersTable.vue'
import { mapGetters, mapMutations } from 'vuex'
import axios from 'axios'
export default {
    name: 'ScraperDashboard',
    components: {
        ScrapersTable,
    },
    data() {
        return {
            refresh_interval: null,
            start_date: null,
            end_date: null,
            name: null,
            url: null,
        }
    },
    computed: {
        ...mapGetters([
            'getStartDate',
            'getEndDate',
            'getURL',
            'getName',
            'getAccessToken',
        ]),
    },

    methods: {
        ...mapMutations(['SET_DATA']),
        resetForm() {
            this.name = null
            this.start_date = null
            this.end_date = null
            this.url = null
        },
        startScraper() {
            axios
                .post(
                    'https://api.inspector-widget.osoc.be:8500/scrapers',
                    {
                        name: this.name,
                        start_date: this.start_date,
                        end_date: this.end_date,
                        url: this.url,
                        status: 'running',
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${this.getAccessToken}`,
                        },
                    }
                )
                .then(console.log('scraper has been added'))

            axios
                .get('https://api.inspector-widget.osoc.be:8500/scrapers/user', {
                    headers: {
                        Authorization: `Bearer ${this.getAccessToken}`,
                    },
                })
                .then((result) => {
                    this.SET_DATA(result.data)
                    this.resetForm()
                })
        },

        updateData() {
            axios
                .get('https://api.inspector-widget.osoc.be:8500/scrapers/user', {
                    headers: {
                        Authorization: `Bearer ${this.getAccessToken}`,
                    },
                })
                .then((result) => this.SET_DATA(result.data))
        },
    },

    mounted() {
        this.refresh_interval = setInterval(this.updateData, 60000)
    },

    unmounted() {
        clearInterval(this.refresh_interval)
    },
}
</script>

<style scoped lang="scss">
.scraper-dashboard {
    padding: 30px;
}
.wider {
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}
.container {
    min-width: 500px;
    margin: 30px auto;
    overflow: auto;
    min-height: 300px;
    border: 5px solid #2782c6;
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
    display: flex;
    align-items: center;
    justify-content: center;
}

.test {
    background-color: #1fabe3;
    color: white;
    margin: 10px;
    border: #1fabe3;
    font-size: 1.25em;
    font-weight: 700;
    &:hover {
        background-color: white;
        margin: 10px;
        font-size: 1.25em;
        font-weight: 700;
        color: #2782c6;
        border-color: #2782c6;
    }
}
</style>
