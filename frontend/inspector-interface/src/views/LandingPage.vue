<template>
<div>
    <div class="container">
     <h1 class="title_message"> WELCOME! </h1>
     </div>
     <div class="container" >
        <login-sign-up />
    </div>
    <div class="container">
        <info-banners />
    </div>
    
</div>
</template>

<script>
import InfoBanners from '../components/InfoBanners.vue'
import LoginSignUp from '../components/LoginSignUp.vue'

export default {
    name: 'LandingPage',
    components: {
        InfoBanners,
        LoginSignUp
    }
}
</script>


<style scoped>

.title_message {
    margin-top: 20px;
    color: #2782C6;
    font-size: 1.50em;
    font-weight: 700;
}

.container {
    margin: auto;
    margin-top: 20px;
}

</style>