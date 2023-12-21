<template>
  <section>
    <div class="card container">
      <h1 class="align-left">Wijzig uw wachtwoord</h1>

      <form @submit="changePassword">
        <div class="align-left">
          <span style="font-weight: 600; color: darkgray"> Oude wachtwoord </span>
        </div>
        <b-field :type="type" class="align-left">
          <b-input v-model="oldPassword" password-reveal required icon-pack="fas" type="password" />
        </b-field>

        <div class="align-left">
          <span style="font-weight: 600; color: darkgray"> Nieuw wachtwoord </span>
        </div>
        <b-field :type="type" class="align-left">
          <b-input v-model="newPassword" password-reveal required icon-pack="fas" type="password" />
        </b-field>

        <div class="align-left">
          <span style="font-weight: 600; color: darkgray"> Nieuwe wachtwoord (verificatie) </span>
        </div>
        <b-field :message="message" :type="type" class="align-left">
          <b-input
            v-model="newPasswordVerify"
            password-reveal
            required
            icon-pack="fas"
            type="password"
          />
        </b-field>
        <b-field class="align-left">
          <b-button native-type="submit" type="is-primary">
            <span style="font-weight: 600">Opslaan</span>
          </b-button>
        </b-field>
      </form>
    </div>
  </section>
</template>

<script>
import { userPasswordUrl } from '@/api'
export default {
  name: 'password-component',
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      newPasswordVerify: '',
      message: '',
      success: false,
    }
  },
  computed: {
    type() {
      if (this.success) {
        return 'is-success'
      } else if (this.message) {
        return 'is-danger'
      } else {
        return 'is-primary'
      }
    },
  },
  methods: {
    changePassword() {
      if (this.newPassword.length < 7) {
        this.message = 'Uw wachtwoord moet tenminste acht karakters lang zijn.'
        return
      }

      if (this.newPassword !== this.newPasswordVerify) {
        this.message = 'De wachtwoorden komen niet overeen.'
        return
      }

      let data = {
        username: this.$store.state.username,
        old_password: this.oldPassword,
        password: this.newPassword,
        password_verify: this.newPasswordVerify,
      }

      this.$http
        .post(userPasswordUrl, data)
        .then((response) => {
          if (response.data.status === true) {
            this.$store.commit('logout')
            this.$router.push('/login')
          } else {
            this.message = response.data.result
          }
        })
        .catch((error) => {
          this.message = error.data.result || JSON.stringify(error)
          this.success = false
        })
    },
  },
}
</script>

<style scoped>
.card {
  max-width: 500px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.7);
}
</style>
