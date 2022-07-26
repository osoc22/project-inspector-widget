<template>
    <div class="container move-down">
        <b-button class="login" @click="goToLogin">Log In </b-button>
        <b-button class="signup" @click="goToSignup" outlined> Sign Up </b-button>
    </div>
</template>


<script>
export default {
    name: 'LoginSignUp',

    methods: {
        goToLogin() {
            this.$router.push('signin')
        },
        goToSignup() {
            this.$router.push('signup')
        }
    }
}
</script>

<style scoped>
.move-down{
    margin-top: 20px;
    margin-left: 30px;
    margin-right: 30px;
    margin-bottom: 20px;
}

.login {
    background-color: #1FABE3;
    color: white;
    margin: 10px;
    border:#1FABE3;
    font-size: 1.25em;
    font-weight: 700;
}

.signup {

    margin: 10px;
    font-size: 1.25em;
    font-weight: 700;
    color: #2782C6;
    border-color: #2782C6;
}
</style>

