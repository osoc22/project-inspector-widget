<template>
<div>
    <div>
     <h1 class="title_message"> WELCOME! </h1>
     </div>
     <div >
        <login-sign-up />
    </div>
    <div>
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

</style>