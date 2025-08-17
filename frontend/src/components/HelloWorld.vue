<template>
  <div class="hello">
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    message: {
      type: String,
      default: 'Ahoj Vue!'
    }
  }
}
</script>

<style scoped>
.hello {
  background: #f6f8fa;
  border-radius: 6px;
  padding: 12px 16px;
  color: #222;
}
</style>
