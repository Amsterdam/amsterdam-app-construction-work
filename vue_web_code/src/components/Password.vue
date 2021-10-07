<template>
  <section>
    <div class="card container">
      <h1>Change password</h1>

      <form @submit="changePassword">
        <b-field
          :type="type"
          label="Old password"
          label-position="on-border">
          <b-input
            v-model="oldPassword"
            password-reveal
            required
            placeholder="Old Password"
            icon-pack="fas"
            type="password"/>
        </b-field>
        <b-field
          :type="type"
          label="New password"
          label-position="on-border">
          <b-input
            v-model="newPassword"
            password-reveal
            required
            placeholder="New Password"
            icon-pack="fas"
            type="password"/>
        </b-field>
        <b-field
          :message="message"
          :type="type"
          label="New password (verify)"
          label-position="on-border">
          <b-input
            v-model="newPasswordVerify"
            password-reveal
            required
            placeholder="New Password (Verify)"
            icon-pack="fas"
            type="password"/>
        </b-field>
        <b-button
          native-type="submit"
          type="is-primary">
          <b-icon
            icon="key"
            pack="fas"/>
          <span>Change password</span>
        </b-button>
      </form>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Password',
  data () {
    return {
      oldPassword: '',
      newPassword: '',
      newPasswordVerify: '',
      message: '',
      success: false
    }
  },
  computed: {
    type: function () {
      if (this.success) {
        return 'is-success'
      } else if (this.message) {
        return 'is-danger'
      } else {
        return 'is-primary'
      }
    }
  },
  methods: {
    changePassword: function () {
      if (this.newPassword.length < 0) {
        this.message = 'Password must be at least 8 characters long'
        return
      }

      if (this.newPassword !== this.newPasswordVerify) {
        this.message = 'Passwords are not the same'
        return
      }

      let data = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
        new_password_verify: this.newPasswordVerify
      }

      this.$http.post('user/password', data)
        .then(response => {
          this.$router.push('/')
        })
        .catch(error => {
          this.message = error.data.message || JSON.stringify(error)
          this.success = false
        })
    }
  }
}
</script>

<style scoped>
.card {
  max-width: 500px;
  padding: 20px;
  background: rgba(255,255,255,0.7);
}
</style>
