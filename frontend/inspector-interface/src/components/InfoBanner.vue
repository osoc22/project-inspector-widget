<template>
<nav class="panel">
  <p class="panel-heading specific_color">
    {{title}}
  </p>
  <div class="panel-block">
    <p class="info"> {{text}}</p>
  </div>

  <div>
    <img
        class="images"
        :src="require('../assets/undraw_authentication_re_svpt.svg')"
        alt="bosa logo"
    />
  </div>
</nav>
</template>

<script>
export default {
    name: 'InfoBanner',

    props: {
        text: String,
        title: String
    }

    

}
</script>

<style scoped>
.specific_color {
  background-color: #2782C6;
  color: white;
}

.info {
  font-size: 20px;
}

.panel {
  height: 660px;
}

</style>

