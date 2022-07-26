<template>
  <div>
    <form @submit="signIn">
      <b-field label="Username">
        <b-input v-model="username" type="text" />
      </b-field>
      <b-field label="Password">
        <b-input v-model="password" type="password" />
      </b-field>
      <b-button
        type="is-primary"
        class="is-block is-fullwidth"
        :disabled="submitDisabled"
        native-type="submit"
      >
        Sign in
      </b-button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import {mapMutations, mapGetters} from 'vuex'
export default {
  name: "SignIn",

  data() {
    return {
      username: null,
      password: null,
      isSubmitting: false,
    };
  },
  computed: {

    ...mapGetters(["getAccessToken", "getRefreshToken"]),
    submitDisabled() {
      return !this.username || !this.password || this.isSubmitting;
    },
  },

  methods: {
    ...mapMutations(['SET_ACCESS_TOKEN', 'SET_REFRESH_TOKEN']),
    signIn(event) {
      event.preventDefault();
      this.isSubmitting = true
      const body = {
          username: this.username,
          password: this.password
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
};
</script>
