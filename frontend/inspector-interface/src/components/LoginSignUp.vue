<template>
    <div class="container move-down">
        <b-button type="is-primary" @click="goToDashboard">Log In </b-button>
        <b-button type="is-primary" outlined> Sign Up </b-button>
    </div>
</template>


<script>
export default {
    name: 'LoginSignUp',

    methods: {
        goToDashboard() {
            this.$router.push('/dashboard')
        }
    }
}
</script>

<style scoped>
.move-down{
    margin-top: 100px;
    margin-left: 30px;
    margin-right: 30px;
}
</style>