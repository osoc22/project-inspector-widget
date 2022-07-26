<template>
  <div id="app">
    <div>
      <header-comp />
    </div>
    <router-view> </router-view>
  
      <footer-comp/>
    
  </div>
</template>

<script>
import FooterComp from './components/FooterComp.vue';
import HeaderComp from "./components/HeaderComp.vue";
export default {
  name: "App",
  components: {
    HeaderComp,
    FooterComp,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
