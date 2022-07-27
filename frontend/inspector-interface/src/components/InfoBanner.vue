<template>
  <nav class="panel">
    <p class="panel-heading specific_color">
      {{ title }}
    </p>
    <div class="panel-block">
      <div class="center">
        <p class="info">{{ text }}</p>
        <img class="images" :src="address" alt="picture" />
      </div>
     
      
    </div>
  </nav>
</template>

<script>
export default {
  name: "InfoBanner",

  props: {
    text: String,
    title: String,
    address: String,
  },
};
</script>

<style scoped>
.specific_color {
  background-color: #2782c6;
  color: white;
}

.info {
  height: 100px;
  font-size: 20px;
}

.panel-block {
  position: relative;  
}

.center {
  margin: auto;
}

.images {
  height: 300px;
  width: auto;
  margin: 10px;
  border: 10px blue !important;
}
</style>
