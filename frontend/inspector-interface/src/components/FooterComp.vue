<template>
  <div>
    <footer>
      <div class="row">
        <div class="row_element">
          <img
            class="images"
            :src="require('/src/assets/BOSA.svg')"
            alt="bosa logo"
          />
        </div>
        <div class="row_element">
          <img
            class="images"
            :src="require('/src/assets/open.svg')"
            alt="bosa logo"
          />
        </div>
        <div class="row_element">
          <img
            class="images"
            :src="require('/src/assets/fod_economie.png')"
            alt="bosa logo"
          />
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: "FooterComp",
};
</script>

<style scoped>
.images {
  object-fit: cover;
  height: 50px;
  width: 100;
  padding: 5px;
 
}

.row_element {
    margin: 50px;
}

.row {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;

}
.divider{
    position:absolute;
    left:50%;
    top:10%;
    bottom:10%;
    border-left:1px solid #2782C6;
}


</style>
