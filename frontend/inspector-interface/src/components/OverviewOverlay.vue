<template>
    <div class="container">
        <p class="panel-heading specific_color">Scraper Info</p>
        <div class="content">
            <b-table :data="[selected_scraper]" :card-layout="true" class="bigger">
                <b-table-column field="id" label="ID" width="40" centered>
                    <p class="text-left">{{ scraper_data.id }}</p>
                </b-table-column>

                <b-table-column centered field="name" label="Scraper Name">
                    <p class="text-left">{{ scraper_data.name }}</p>
                </b-table-column>

                <b-table-column field="url" label="URL" centered>
                    <p class="text-center">{{ scraper_data.url }}</p>
                </b-table-column>

                <b-table-column field="status" label="Status" centered>
                    <span
                        class="tag"
                        :class="{
                            'is-success': scraper_data.status.toUpperCase() == 'DONE',
                            'is-warning': scraper_data.status.toUpperCase() == 'RUNNING',
                            'is-danger': scraper_data.status.toUpperCase() == 'ERROR',
                        }"
                    >
                        <p class="text-left">{{ scraper_data.status }}</p>
                    </span>
                </b-table-column>

                <b-table-column field="start_date" label="Start Date" centered>
                    <p class="text-center">{{ scraper_data.start_date }}</p>
                </b-table-column>

                <b-table-column field="end_date" label="End Date" centered>
                    <p class="text-center">{{ scraper_data.end_date }}</p>
                </b-table-column>

                <b-table-column field="last_scanned" label="Last Scanned" centered>
                    <p class="text-center">{{ scraper_data.last_scanned }}</p>
                </b-table-column>

                <b-table-column field="last_scanned" label="Last Scanned" centered>
                    <p class="text-center">{{ scraper_data.last_scanned }}</p>
                </b-table-column>

                <b-table-column field="webshop" label="Webshop" centered>
                    <p class="text-center">{{ scraper_data.webshop }}</p>
                </b-table-column>

                <b-table-column field="owner" label="Owner" centered>
                    <p class="text-center">{{ scraper_data.owner }}</p>
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
                    </div>
                </b-table-column>
                <b-table-column centered>
                    <b-button
                        @click="() => deleteScraper(scraper_data.id)"
                        size="is-small"
                        rounded
                        outlined
                        type="is-danger"
                    >
                        DELETE
                    </b-button>
                </b-table-column>
            </b-table>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import axios from 'axios'
import { saveAs } from 'file-saver'
export default {
    name: 'OverviewOverlay',

    computed: {
        ...mapGetters(['getData', 'getAccessToken']),
    },
    props: {
        scraper_data: {
            type: Object,
            default: null,
            required: true,
        },
        closeOverview: {
            type: Function,
            default: () => {},
            required: true,
        },
    },

    methods: {
        ...mapMutations(['SET_DATA']),
        deleteScraper(id) {
            const delete_request =
                'https://bosa-inspector-widget.herokuapp.com/scrapers/' + id.toString()
            console.log('this should delete the scraper')
            axios.delete(delete_request, {
                headers: {
                    Authorization: `Bearer ${this.getAccessToken}`,
                },
            })
            axios
                .get('https://bosa-inspector-widget.herokuapp.com/scrapers/user', {
                    headers: {
                        Authorization: `Bearer ${this.getAccessToken}`,
                    },
                })
                .then((result) => {
                    this.SET_DATA(result.data)
                    this.closeOverview()
                })
        },
        downloadResults(id) {
            const download_request =
                'https://bosa-inspector-widget.herokuapp.com/scrapers/' +
                id.toString() +
                '/export'
            console.log('this should download the results')

            axios
                .get(download_request, {
                    headers: {
                        Authorization: `Bearer ${this.getAccessToken}`,
                    },
                    responseType: 'blob',
                })
                .then((res) => {
                    saveAs(res.data, res.headers['x-filename']) //file-saver npm package
                })
        },
    },
}
</script>

<style scoped>
.container {
    margin: 30px auto;
    overflow: auto;
    position: relative;
    top: 30px;
}

.content {
    min-width: 600px;
    padding: 50px;
    background-color: white;
}

.alignRight {
    text-align: right;
}
</style>
