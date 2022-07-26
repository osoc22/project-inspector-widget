<template>
  <div class="columns move-down">
    <div class="column">
      <info-banner
        text="Please login if you are a user, or signup if this is the first time you are using the application (you can login/signup using the buttons below)"
      />
    </div>
    <div class="column">
      <info-banner
        text="Please login if you are a user, or signup if this is the first time you are using the application (you can login/signup using the buttons below)"
      />
    </div>
    <div class="column">
      <info-banner
        text="Please login if you are a user, or signup if this is the first time you are using the application (you can login/signup using the buttons below)"
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
  margin-top: 100px;
  margin-left: 30px;
  margin-right: 30px;
}
</style>
