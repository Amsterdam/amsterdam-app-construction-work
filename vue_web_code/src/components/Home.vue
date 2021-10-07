<template>
  <section>
    <div class="outer-section">
      <h1 class="is-size-2">
        Welcome, {{ $store.state.username }}
      </h1>
      <p>
        This is a template application waiting to be extended into something really nice :)
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style>
.outer-section {
  margin: 125px;
  background: rgba(255,255,255,0.0);
}
</style>
