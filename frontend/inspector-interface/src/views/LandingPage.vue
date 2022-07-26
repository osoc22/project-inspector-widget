<template>
<div>
    <div>
        <info-banners />
    </div>
    <div class="container">
        <login-sign-up />
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