<template>
<nav class="panel">
  <p class="panel-heading specific_color">
    STEP 1
  </p>
  <div class="panel-block">
    <p> {{text}}</p>
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
    }

    

}
</script>

<style scoped>
.specific_color {
  background-color: #2782C6;
  color: white;
}

</style>

