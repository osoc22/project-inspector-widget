<template>
    <b-navbar class="bar">
        <template #brand>
            <b-navbar-item @click="goToLanding">
                <img
                    src='../assets/2560px-Logo-fr-SPF-economie.png'
                    alt="Lightweight UI components for Vue.js based on Bulma"
                >
            </b-navbar-item>
        </template>
    </b-navbar>
</template>


<script>
export default {
    name: 'HeaderComp',

    methods: {
        goToLanding() {
            this.$router.replace('/')
        }
    }

}
</script>

<style scoped>
.bar{
    background-color: #D43E25;
}
</style>