<template>
  <div class="card-center-container">
    <div class="card-center">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardCenter'
}
</script>

<style scoped>
.card-center-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  padding: 2rem;
}

.card-center {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  width: 100%;
  max-width: 420px;
}
</style>
