<template>
  <div class="login_container">
    <nav class="panel">
      <p class="panel-heading specific_color">Please Sign Up</p>
      <div class="spacious">
        <form class="signup-form pb-5 mb-5" @submit="signUp">
          <b-field label="Username">
            <b-input v-model="username" type="text" class="input_field" />
          </b-field>

          <b-field label="Email" class="mb-5">
            <b-input v-model="email" type="email" class="input_field" />
          </b-field>
          <b-field
            label="Password"
            message="Use a password with at least 6 characters."
          >
            <b-input v-model="password" type="password" class="input_field" />
          </b-field>
          <b-button
            type="is-primary"
            class="signin_button"
            :disabled="!submitDisabled"
            native-type="submit"
          >
            Sign up
          </b-button>
        </form>
      </div>
    </nav>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignUp",
  data() {
    return {
      username: null,
      email: null,
      password: null,
      isSubmitting: false,
    };
  },
  computed: {
    submitDisabled() {
      return (
        !this.email ||
        !this.password ||
        !this.firstname ||
        !this.lastname ||
        this.isSubmitting
      );
    },
  },
  methods: {
    signUp(event) {
      event.preventDefault();
      this.isSubmitting = true;
      const body = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      axios
        .post("https://bosa-inspector-widget.herokuapp.com/register", body)
        .then(() => {
          this.confirmed = true;
          this.$router.push("/login");
        })
        .catch(() => {
          this.error = true;
        });
      console.log("this should have added to username");
    },
  },
};
</script>
