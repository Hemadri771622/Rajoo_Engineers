<template>
  <div class="app">
    <!-- LEFT SIDEBAR -->
    <Sidebar />
    <!-- MAIN -->
    <main class="main">
      <!-- TOP BAR -->
      <header class="topbar">
        <!-- LEFT TITLE -->
        <div class="top-left">
          <h1>THREE LAYER BLOWN FILM LINE</h1>
        </div>

        <!-- CENTER KPI BOXES -->
        <div class="top-kpi-wrapper">
          <div class="top-kpi-box">
            <div class="kpi-title">OEE</div>
            <div class="kpi-value">{{ oee ?? 'N/A' }}</div>
          </div>

          <div class="top-kpi-box">
            <div class="kpi-title">Availability</div>
            <div class="kpi-value">{{ availability ?? 'N/A' }}</div>
          </div>

          <div class="top-kpi-box">
            <div class="kpi-title">Performance</div>
            <div class="kpi-value">{{ performance ?? 'N/A' }}</div>
          </div>

          <div class="top-kpi-box">
            <div class="kpi-title">Quality</div>
            <div class="kpi-value">{{ quality ?? 'N/A' }}</div>
          </div>
        </div>

        <!-- RIGHT DATE + ICONS -->
        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />
            {{ currentTime }}
          </span>
          <img src="/notification.png" class="notification-icon" />
          <img src="/power-button.png" class="power-icon" @click="handleLogout" />
        </div>

      </header>

      <!-- CONTENT -->
      <div class="content">
        <!-- LEFT PANEL -->
        <section class="panel left-panel">
          <slot />
        </section>

        <!-- RIGHT PANEL (OEE) -->
        <!-- <section class="panel right-panel">
          <h2>OVERALL EQUIPMENT EFFICIENCY</h2>
          <div class="oee-grid">
            <div class="oee-box">OEE <span>72%</span></div>
            <div class="oee-box">Availability <span>87%</span></div>
            <div class="oee-box">Performance <span>81%</span></div>
            <div class="oee-box">Quality <span>94%</span></div>
          </div>
        </section> -->
      </div>

      <!-- FOOTER -->
      <footer class="footer">
        MODEL : RFC-2550-40-1800
      </footer>
    </main>
  </div>
</template>

<script>
import Sidebar from './Sidebar.vue';

export default {
  name: "LayerLayout",
  components: { Sidebar },
  props: {
    title: String
  },
  data() {
    return {
      currentDate: "",
      currentTime: ""
    };
  },
  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);
  },
  methods: {
    updateClock() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-GB");
      this.currentTime = now.toLocaleTimeString("en-US");
    }
  }
};
</script>

<style>
/* .topbar {
  height: 60px;
  min-height: 60px;
  max-height: 60px;
  flex-shrink: 0;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #0e2f43, #081c28);
  overflow: hidden;
}

.topbar h1 {
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
} */

.top-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.notification-icon,
.power-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  cursor: pointer;
}

.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #9ecfff;
}

.back-icon {
  width: 36px;
  height: 36px;
  cursor: pointer;
  border-radius: 50%;
  padding: 6px;
  background: rgba(0, 255, 160, 0.12);
  transition: 0.2s ease;
}

.back-icon:hover {
  transform: scale(1.05);
  background: rgba(0, 255, 160, 0.18);
}
</style>