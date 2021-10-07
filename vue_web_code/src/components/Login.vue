<template>
  <section>
    <div
      class="card login"
      @submit="login">
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
      <form>
        <b-field
          :type="message ? 'is-danger' : 'is-primary'"
          message="Voer uw gebruikersnaam in">
          <b-input
            v-model="username"
            placeholder="Gebruikersnaam"
            required/>
        </b-field>
        <b-field
          :type="message ? 'is-danger' : 'is-primary'"
          message="Voer uw wachtwoord in">
          <b-input
            v-model="password"
            password-reveal
            required
            icon-pack="fas"
            placeholder="Wachtwoord"
            type="password"/>
        </b-field>
        <b-button
          native-type="submit"
          type="is-primary">
          <b-icon
            icon="sign-in-alt"
            pack="fas"/>
          <span>Aanmelden</span>
        </b-button>
      </form>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      message: ''
    }
  },
  mounted () {
    console.log('Vue code mounted in login()')
  },
  methods: {
    async login () {
      let data = {
        username: this.username,
        password: this.password
      }

      this.$http.post('get-token/', data).then(response => {
        console.log(response.data)
        if (response.data.error) {
          this.message = JSON.stringify(response.data.error)
        } else {
          this.$http.defaults.headers.common['Authorization'] = response.data.access
          this.$store.commit('login', {
            refresh: response.data.refresh,
            access: response.data.access,
            username: data.username
          })
        }
        this.$router.push('/')
      })
    }
  }
}
</script>

<style>
.spacer {
  margin: 15px;
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
