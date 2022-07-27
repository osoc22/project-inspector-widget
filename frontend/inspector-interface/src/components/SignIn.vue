<template>
    <div class="login_container">
        <nav class="panel">
            <p class="panel-heading specific_color">Please Login</p>
            <div class="spacious">
                <form @submit="signIn">
                    <b-field label="Username">
                        <b-input v-model="username" type="text" class="input_field" />
                    </b-field>
                    <b-field label="Password">
                        <b-input v-model="password" type="password" class="input_field" />
                    </b-field>
                    <b-button
                        class="signin_button"
                        :disabled="submitDisabled"
                        native-type="submit"
                    >
                        Sign in
                    </b-button>
                </form>
            </div>
        </nav>
    </div>
</template>

<script>
import axios from 'axios'
import { mapMutations, mapGetters } from 'vuex'
export default {
    name: 'SignIn',

    data() {
        return {
            username: null,
            password: null,
            isSubmitting: false,
        }
    },
    computed: {
        ...mapGetters(['getAccessToken', 'getRefreshToken']),
        submitDisabled() {
            return !this.username || !this.password || this.isSubmitting
        },
    },

    methods: {
        ...mapMutations(['SET_ACCESS_TOKEN', 'SET_REFRESH_TOKEN']),
        signIn(event) {
            event.preventDefault()
            this.isSubmitting = true
            const body = {
                username: this.username,
                password: this.password,
            }
            axios
                .post('https://bosa-inspector-widget.herokuapp.com/login', body)
                .then((user_res) => {
                    this.SET_ACCESS_TOKEN(user_res.data.access_token)
                    this.SET_REFRESH_TOKEN(user_res.data.refresh_token)
                    console.log(this.getAccessToken)
                    this.$router.push('dashboard')
                })
                .catch(() => {
                    this.error = true
                })
        },
    },
}
</script>

<style lang="scss">
.specific_color {
    background-color: #1fabe3;
    color: white;
}

.info {
    font-size: 20px;
}

.login_container {
    margin: auto;
    margin-top: 20px;
    max-width: 50%;
}

.signin_button {
    margin: 10px;
    background-color: #2782c6 !important;
    width: 250px;
    color: white;
    font-size: 20px;
    font-weight: 700;
}

.input_field {
    & input:focus {
        border-color: #1fabe3 !important;
        box-shadow: 0 0 0 0.125em rgba(31, 171, 227, 0.25) !important;
    }
}

.spacious {
    margin: auto;
    width: 85%;
    margin-top: 20px;
}
</style>
