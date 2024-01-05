<template>
  <div id="app">
    <div v-if="this.$store.state.isLoggedIn" class="hero is-small is-white">
      <div class="hero-body">
        <div class="columns">
          <div class="column is-offset-2 is-flex">
            <a href="https://amsterdam.nl">
              <img style="margin-left: -30px" alt="Gemeente Amsterdam" src="@/assets/logo.svg" />
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="content">
      <navigation v-if="this.$store.state.isLoggedIn" />
      <div class="columns">
        <div class="column is-offset-2 is-flex">
          <router-view class="container" />
        </div>
        <div class="column is-2" />
      </div>
    </div>
  </div>
</template>

<script>
import Navigation from '@/components/Navigation.vue'

export default {
  name: 'App',
  components: { Navigation },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.content {
  flex: 1;
}

.container {
  padding-top: 30px;
}
</style>
