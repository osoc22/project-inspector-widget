<template>
<div class="input">
    <b-field label="Select a period">
        <b-datepicker
            placeholder="Click to select..."
            v-model="dates"
            range
            @range-start="retrieveDates"
            @range-end="retrieveDates">
        </b-datepicker>
       
    </b-field>

</div>
</template>

<script>
export default {
    name : 'DateSelector',
    data() {
        return {
            dates: []
        }
    },
    methods: {
        retrieveDates(input) {
            if (this.dates.length >= 2){
                this.dates = []
            }
            this.dates.push(input)   
        }
        
    }
}
</script>

<style scoped>
.input { 
    margin: 10px auto;
    width: 100%;
    padding: 50px;
    }
</style>



