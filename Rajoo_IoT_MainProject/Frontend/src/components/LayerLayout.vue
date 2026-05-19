<template>
  <div class="app">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" @click="$router.push('/layer1')">Layer 1</button>
        <button class="menu-item" @click="$router.push('/layer2')">Layer 2</button>
        <button class="menu-item" @click="$router.push('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item">Extruder 1</button>
        <button class="menu-item">Extruder 2</button>
        <button class="menu-item">Extruder 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item">Winder 1</button>
        <button class="menu-item">Winder 2</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>
        <button class="menu-item">Reports</button>
        <button class="menu-item">Material Utilization</button>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main">
      <!-- TOP BAR -->
      <header class="topbar">
        <h1>{{ title }}</h1>
        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />
            {{ currentTime }}
          </span>
          <img src="/notification.png" class="notification-icon" />
          <img
            src="/power-button.png"
            class="power-icon"
            @click="$emit('logout')"
          />
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
export default {
  name: "LayerLayout",
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
