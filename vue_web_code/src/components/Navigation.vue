<template>
  <div class="columns">
    <div class="column is-2 is-gapless amsterdam_grey"/>
    <div class="column is-gapless is_not_spaced">
      <b-navbar
        v-if="logged_in"
        :key="update">
        <template slot="start">
          <b-navbar-item
            class="is-active"
            tag="router-link"
            to="/">
            <span
              v-if="this.$router.currentRoute.path === '/'"
              class="active-link"
              style="font-weight: bolder">Accountbeheer</span>
            <span
              v-else
              class="underline-on-hover inactive-link"
              style="font-weight: bolder">Accountbeheer</span>
          </b-navbar-item>

          <b-navbar-item
            class="is-active"
            tag="router-link"
            to="/BerichtenBeheer">
            <span
              v-if="this.$router.currentRoute.path === '/BerichtenBeheer'"
              class="active-link"
              style="font-weight: bolder">Berichtenbeheer</span>
            <span
              v-else
              class="underline-on-hover inactive-link"
              style="font-weight: bolder">Berichtenbeheer</span>
          </b-navbar-item>
        </template>

        <template slot="end">
          <b-navbar-dropdown
            :label="$store.state.username"
            style="font-weight: bolder"
            right>
            <b-navbar-item
              tag="router-link"
              to="/password">
              Wijzig wachtwoord
            </b-navbar-item>
            <b-navbar-item @click.native="logout">
              Afmelden
            </b-navbar-item>
          </b-navbar-dropdown>
        </template>
      </b-navbar>
    </div>
    <div class="column is-2 is-gapless amsterdam_grey"/>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  data () {
    return {
      logged_in: this.$store.state.isLoggedIn,
      current_path: null,
      update: 0
    }
  },
  watch: {
    '$route' (to, from) {
      if (this.$router.currentRoute.path !== this.current_path) {
        this.current_path = this.$router.currentRoute.path
        this.update += 1
      }
    }
  },
  methods: {
    logout: function () {
      this.$http.defaults.headers.common['Authorization'] = ''
      this.$store.commit('logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.is_not_spaced {
  margin: 0;
  padding: 0;
}

.underline-on-hover:hover {
  border-bottom: 2px solid black;
}

.active-link {
  border-bottom: 2px solid #E50617;
  display: inline-block;
}

.inactive-link {
  display: inline-block;
}
</style>
