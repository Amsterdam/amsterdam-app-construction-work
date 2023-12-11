<template>
  <div>
    <div
      class="card login">
      <div>
        <div style="text-align: left">
          <a
            class="mainlogo"
            href="https://www.amsterdam.nl">
            <img
              src="@/assets/logo.svg"
              alt="Gemeente Amsterdam">
          </a>
        </div>
        <div class="spacer"/>
      </div>
      <form
        @submit="login">
        <div
          class="align-left margin-less">
          <span
            class="align-left"
            style="font-weight: 600; color: darkgray">
            Voer uw gebruikersnaam in
          </span>
        </div>
        <b-field
          :type="message ? 'is-danger' : 'is-primary'">
          <b-input
            ref="inputUsername"/>
        </b-field>
        <div
          class="align-left margin-less">
          <span
            class="align-left"
            style="font-weight: 600; color: darkgrey">
            Voer uw wachtwoord in
          </span>
        </div>
        <b-field
          :type="message ? 'is-danger' : 'is-primary'">
          <b-input
            ref="inputPassword"
            type="password"/>
        </b-field>
        <div
          v-if="!!message"
          class="align-left margin-less">
          <span
            class="align-left"
            style="font-weight: 600; color: darkgrey">
            {{ message }}
          </span>
        </div>
        <b-button
          native-type="submit"
          type="is-primary">
          <b-icon
            icon="sign-in-alt"
            pack="fas"/>
          <span style="font-weight: 600;">Aanmelden</span>
        </b-button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data () {
    return {
      message: ''
    }
  },
  mounted () {
    console.log('Vue code mounted in login()')
  },
  methods: {
    login () {
      let data = {
        username: this.$refs.inputUsername.newValue,
        password: this.$refs.inputPassword.newValue
      }
      axios.post('/get-token/', {
        username: this.$refs.inputUsername.newValue,
        password: this.$refs.inputPassword.newValue
      }).then(response => {
        console.log(1, response)
        this.$store.commit('login', {
          refresh: response.data.refresh,
          access: response.data.access,
          username: data.username
        })
        this.$router.push('/')
      }).catch((err) => {
        console.log(err)
        this.message = `${err.status}: ${err.statusText}`
      })
    }
  }
}
</script>

<style>
.spacer {
  margin: 15px;
}

.margin-less {
  margin: 0;
  padding: 0;
}

.login {
    flex-grow: 1;
    margin: 0 auto;
    position: relative;
    width: 600px;
}

body {
  background-image: url('~@/assets/background.jpg');
  background-size: cover;
  min-width: 100%;
  background-repeat: no-repeat;
  background-position: center center;
}
</style>
