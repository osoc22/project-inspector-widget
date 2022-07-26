<template>
  <div class="columns move-down">
    <div class="column">
      <info-banner
        title= "STEP 1"
        text="Please login if you are a user, or signup if this is the first time you are using the application"
      />
    </div>
    <div class="column">
      <info-banner
        title="STEP 2"
        text="Insert the URL of the product page you want to scan and select the duration of the scan"
      />
    </div>
    <div class="column">
      <info-banner
        title="STEP 3" 
        text="Download the results and view suspicious products"
      />
    </div>
  </div>
</template>

<script>
import InfoBanner from "./InfoBanner.vue";

export default {
  name: "InfoBanners",

  components: {
    InfoBanner,
  },
};
</script>

<style scoped>
.move-down {
  margin-top: 20px;
  margin-left: 30px;
  margin-right: 30px;
}
</style>
