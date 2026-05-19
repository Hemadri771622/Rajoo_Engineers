<template>
  <header class="topbar">

    <!-- LEFT SECTION -->
    <div class="top-left">

      <!-- Back Button (only if enabled) -->
      <img
        v-if="showBack"
        src="/back-arrow.png"
        class="back-icon"
        @click="$emit('back')"
      />

      <h1 class="page-title">
        {{ title }}
      </h1>
    </div>

    <!-- CENTER KPI (only if provided) -->
    <div v-if="hasKpis" class="top-kpi-wrapper">
      <div
        v-for="kpi in kpis"
        :key="kpi.label"
        class="top-kpi-box"
      >
        <div class="kpi-title">{{ kpi.label }}</div>
        <div class="kpi-value">
          {{ kpi.value ?? "N/A" }}
        </div>
      </div>
    </div>

    <!-- RIGHT SECTION -->
    <div class="top-right">

      <span class="pill dark">
        {{ currentDate }}<br />
        {{ currentTime }}
      </span>

      <img
        src="/notification.png"
        class="notification-icon"
      />

      <!-- Logout only if KPI mode (dashboard) -->
      <img
        v-if="hasKpis"
        src="/power-button.png"
        class="power-icon"
        @click="$emit('logout')"
      />
    </div>

  </header>
</template>

<script>
export default {
  name: "AppHeader",

  props: {
    title: {
      type: String,
      required: true
    },
    showBack: {
      type: Boolean,
      default: false
    },
    kpis: {
      type: Array,
      default: null
    }
  },

  data() {
    return {
      currentDate: "",
      currentTime: "",
      clockInterval: null
    };
  },

  computed: {
    hasKpis() {
      return this.kpis && this.kpis.length > 0;
    }
  },

  mounted() {
    this.updateClock();
    this.clockInterval = setInterval(this.updateClock, 1000);
  },

  beforeUnmount() {
    if (this.clockInterval) {
      clearInterval(this.clockInterval);
      this.clockInterval = null;
    }
  },

  methods: {
    updateClock() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-GB");
      this.currentTime = now.toLocaleTimeString("en-GB");
    }
  }
};
</script>

<style scoped>

/* ================= TOP BAR ================= */

.topbar {
  height: 60px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #0e2f43, #081c28);
}

/* ================= LEFT ================= */

.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  text-transform: uppercase;
  line-height: 1;
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

.back-icon {
  width: 32px;
  height: 32px;
  cursor: pointer;
}

/* ================= KPI CENTER ================= */

.top-kpi-wrapper {
  display: flex;
  gap: 14px;
  align-items: center;
}

.top-kpi-box {
  min-width: 110px;
  padding: 6px 12px;
  border-radius: 12px;
  background: rgba(255,255,255,0.12);
  text-align: center;
}

.kpi-title {
  font-size: 11px;
  opacity: 0.8;
}

.kpi-value {
  font-size: 16px;
  font-weight: 700;
}

/* ================= RIGHT ================= */

.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.notification-icon,
.power-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

</style>