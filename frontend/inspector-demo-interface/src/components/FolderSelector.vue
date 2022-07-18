<template>
    <b-field class="file is-warning" :class="{'has-name': !!file}">
        <b-upload v-model="file" class="file-label" @input="registerDestination"
         rounded=true>
            <span class="file-cta">
                <b-icon class="file-icon " icon="upload"></b-icon>
                <span class="file-label ">{{text}}</span>
            </span>
            <span class="file-name" v-if="file">
                {{ file.name }}
            </span>
        </b-upload>
    </b-field>
</template>

<script>
    export default {
        name : "FolderSelector.vue",
        data() {
            return {
                file: null
            }
        },
        props: {
            text: String
        },

        methods: {
            registerDestination(input){
                this.file = input
                console.log(this.file)
            }
        }
    }
</script>



