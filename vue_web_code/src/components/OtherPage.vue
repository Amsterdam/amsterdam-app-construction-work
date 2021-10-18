<template>
  <div class="outer-section">
    <section>
      <h1>Welcome, {{ $store.state.username }}</h1>
      <p>Simple landing page for now...</p>
    </section>
  </div>
</template>

<script>
export default {
  data () {
    return {}
  },
  methods: {}
}
</script>

<style>
section {
  margin: 25px;
}

.outer-section {
  margin: 125px;
  background: rgba(255,255,255,1.0);
}
</style>
