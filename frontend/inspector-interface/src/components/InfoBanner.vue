<template>
<nav class="panel is-danger">
  <p class="panel-heading">
    STEP 1
  </p>
  <div class="panel-block">
    <p> {{text}}</p>
  </div>
</nav>
</template>

<script>
export default {
    name: 'InfoBanner',

    props: {
        text: String
    }

    

}
</script>

<style scoped>

</style>

