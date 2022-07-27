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
        <template #end v-if="getAccessToken">
            <b-button class="plain" @click="disconnect">
                <h1 class="header_title"> Log Out 
                    </h1>

                </b-button>
        </template>
    </b-navbar>
</template>


<script>
import {mapActions, mapGetters} from 'vuex'
export default {
    name: 'HeaderComp',

    computed: {
        ...mapGetters(["getAccessToken"])
    },

    methods: {
        ...mapActions(['disconnect']),
        goToLanding() {
            this.$router.push({name:'home'})
        }
    }

}
</script>

<style scoped lang="scss">
.bar{
    background-color: #2782C6;
    display: flex;
    align-items: center;
    padding-right: 10px;
}

.header_title {
    color: white;
    font-size: 1.50em;
    font-weight: 700;
    &:hover {
        color: whitesmoke;

    }
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