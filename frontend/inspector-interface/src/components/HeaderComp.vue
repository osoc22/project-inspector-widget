<template>
    <b-navbar class="bar">
        <template #brand>
            <b-navbar-item @click="goToLanding">
                <h1 class="header_title">Inspector Widget </h1>
            </b-navbar-item>
            <b-navbar-item>    
                <img
                    class="images"
                    :src="require('/src/assets/osoc-2.svg')"
                    alt="osoc logo"
                />
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

<style scoped lang="scss">
.bar{
    background-color: #2782C6;
}

.header_title {
    color: white;
    font-size: 1.50em;
    font-weight: 700;
    &:hover {
        color: whitesmoke;

    }
}
</style>