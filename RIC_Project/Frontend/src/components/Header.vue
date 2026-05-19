<template>
  <header class="topbar">

    <!-- LEFT SIDE -->
    <div class="top-left">

      <div class="back-icon" @click="goBack">
        <span class="material-icons">home</span>
      </div>

      <!-- TITLE -->
      <h1>THREE LAYER BLOWN FILM LINE</h1>

    </div>

    <!-- RIGHT SIDE -->
    <div class="top-right">

      <!-- RAJOO LOGO -->
      <div class="rajoo-logo-box">
        <img src="/rajoo_logo.png" alt="Rajoo Logo" />
      </div>

      <!-- DATE TIME -->
      <span class="pill dark">
        {{ currentDate }}<br />
        {{ currentTime }}
      </span>

      <!-- NOTIFICATION -->
      <div class="notification-icon">
        <span class="material-icons">notifications</span>
      </div>

    </div>

  </header>
</template>

<script>
export default {
  name: "Header",

  data() {
    return {
      currentDate: "",
      currentTime: "",
      clockInterval: null
    };
  },

  mounted() {
    this.updateClock();

    this.clockInterval = setInterval(() => {
      this.updateClock();
    }, 1000);
  },

  beforeUnmount() {
    if (this.clockInterval) {
      clearInterval(this.clockInterval);
    }
  },

  methods: {
    goBack() {
      this.$router.push("/dashboard");
    },

    updateClock() {
      const d = new Date();

      this.currentDate = d.toLocaleDateString("en-GB");

      this.currentTime = d.toLocaleTimeString("en-GB", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
      });
    }
  }
};
</script>

<style scoped>
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 10px 16px;

  background: linear-gradient(
    180deg,
    rgba(14,47,67,0.96),
    rgba(8,28,40,0.96)
  );

  backdrop-filter: blur(10px);

  border-bottom: 1px solid rgba(127,220,255,0.10);
}

/* LEFT SIDE */
.top-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* HOME ICON */
.back-icon {
  width: 40px;
  height: 40px;

  border-radius: 12px;

  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;

  background: rgba(255,255,255,0.08);

  border: 1px solid rgba(255,255,255,0.10);

  color: #dff6ff;

  transition: all 0.25s ease;
}

.back-icon:hover {
  transform: translateY(-1px);

  background: rgba(127,220,255,0.14);

  box-shadow:
    0 0 12px rgba(127,220,255,0.18);
}

/* TITLE */
.top-left h1 {
  margin: 0;

  font-size: 20px;
  font-weight: 700;

  letter-spacing: 0.4px;

  background: linear-gradient(
    90deg,
    #e6f7fb 0%,
    #7fdcff 40%,
    #4dd0e1 70%,
    #e6f7fb 100%
  );

  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* RIGHT SIDE */
.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* RAJOO LOGO */
.rajoo-logo-box {
  height: 42px;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 4px 10px;

  border-radius: 12px;

  background: rgba(255,255,255,0.06);

  border: 1px solid rgba(255,255,255,0.08);

  backdrop-filter: blur(6px);

  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.06);
}

.rajoo-logo-box img {
  height: 28px;
  width: auto;

  object-fit: contain;

  display: block;
}

/* DATE TIME */
.pill.dark {
  padding: 6px 12px;

  border-radius: 12px;

  font-size: 12px;
  font-weight: 600;

  color: #fff;

  background: rgba(255,255,255,0.08);

  border: 1px solid rgba(255,255,255,0.08);

  text-align: center;
  line-height: 1.3;

  backdrop-filter: blur(6px);
}

/* NOTIFICATION */
.notification-icon {
  width: 42px;
  height: 42px;

  border-radius: 14px;

  background: rgba(255,255,255,0.08);

  border: 1px solid rgba(255,255,255,0.10);

  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;

  color: #dff6ff;

  transition: all 0.25s ease;
}

.notification-icon:hover {
  transform: translateY(-1px);

  background: rgba(127,220,255,0.14);

  box-shadow:
    0 0 12px rgba(127,220,255,0.18);
}
</style>