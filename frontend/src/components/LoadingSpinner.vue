<template>
  <div class="loading-spinner">
    <div class="spinner"></div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner'
}
</script>

<style scoped>
.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-right: 8px;
}

.spinner {
  width: 100%;
  height: 100%;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #333;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
