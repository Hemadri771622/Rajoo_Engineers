<template>
  <button class="back-btn" @click="goBack">
    ⬅ Back
  </button>
</template>

<script>
export default {
  name: "BackToDashboard",
  methods: {
    goBack() {
        this.$router.push({
        path: "/dashboard",
        meta: { transition: "slide-back" }
        });
        }
    }
};
</script>

<style scoped>
.back-btn {
  padding: 8px 16px;
  background-color: #2c3e50;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.back-btn:hover {
  background-color: #1a252f;
}
</style>
