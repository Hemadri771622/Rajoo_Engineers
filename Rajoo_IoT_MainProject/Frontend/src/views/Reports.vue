<template>
  <div class="app">
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" :class="{ active: isActive('/layer1') }" @click="navigate('/layer1')">Layer 1</button>
        <button class="menu-item" :class="{ active: isActive('/layer2') }" @click="navigate('/layer2')">Layer 2</button>
        <button class="menu-item" :class="{ active: isActive('/layer3') }" @click="navigate('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" @click="navigate('/extruder1')">Extruder A</button>
        <button class="menu-item" @click="navigate('/extruder2')">Extruder B</button>
        <button class="menu-item" @click="navigate('/extruder3')">Extruder C</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item" @click="navigate('/winder1')">Winder 1</button>
        <button class="menu-item" @click="navigate('/winder2')">Winder 2</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>
        <button class="menu-item" @click="navigate('/reports')">Reports</button>
        <button class="menu-item" @click="navigate('/material-utilization')">Material Utilization</button>
      </div>
    </aside>

    <main class="main">
      <header class="topbar">
  <div class="top-left">
    <img src="/back-arrow.png" class="back-icon" @click="goBack" />
    <h1 class="page-title">THREE LAYER BLOWN FILM LINE</h1>
  </div>

  <div class="top-right">
    <span class="pill dark">
      {{ currentDate }}<br />
      {{ currentTime }}
    </span>
    <img src="/notification.png" class="notification-icon" />
    <!-- <img src="/power-button.png" class="power-icon" /> -->
  </div>
</header>

      <div class="content">
        <section class="panel left-panel">
        <h2>REPORTS</h2>

  <!-- ONLY THIS BLOCK IS NEW -->
  <div class="report-container">
    <div class="report-box">

      <button class="report-btn" @click="openReport('production')">
        PRODUCTION REPORT
      </button>

      <button class="report-btn" @click="openReport('thickness')">
        THICKNESS PROFILE REPORT
      </button>

      <button class="report-btn" @click="openReport('material')">
        MATERIAL UTILISATION REPORT
      </button>

    </div>
  </div>

</section>
      </div>

      <footer class="footer">MODEL : RFC-2550-40-1800</footer>
    </main>
  </div>
</template>


<script>
export default {
  name: "Reports",
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
    navigate(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },

    goBack() {
      this.$router.push("/dashboard");
    },

    isActive(path) {
      return this.$route.path === path;
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    },

    /* OPEN ONLY LATEST REPORT FROM FOLDER */
   async openReport(type) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/latest/${type}`);
    const data = await response.json();

    if (!data.path) {
      alert("No report available yet.");
      return;
    }

    // IMPORTANT: open from frontend server (5173), not backend
    const frontendUrl = `http://127.0.0.1:5173${data.path}?t=` + new Date().getTime();

    window.open(frontendUrl, "_blank");

  } catch (error) {
    console.error("Error fetching report:", error);
    alert("Unable to load report.");
  }
}
  }
};
</script>

<style scoped>

.content {
  flex: 1;
  display: flex;
}

.panel.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* ================= TOPBAR ================= */

.topbar {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background: linear-gradient(180deg, #0e2f43, #081c28);
  overflow: hidden;
}

/* LEFT SIDE */
.top-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

/* Back Button (Fixed Size) */
.back-icon {
  width: 26px;
  height: 26px;
  padding: 3px;
  cursor: pointer;
  border-radius: 50%;
  flex-shrink: 0;

  background: rgba(0, 255, 160, 0.08);
  transition: all 0.2s ease;
}

.back-icon:hover {
  background: rgba(0, 255, 160, 0.18);
  transform: scale(1.05);
}

/* Title */
.page-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  background: linear-gradient(
    90deg,
    #e6f7fb 0%,
    #7fdcff 50%,
    #4dd0e1 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* RIGHT SIDE */
.top-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.notification-icon,
.power-icon {
  width: 22px;
  height: 22px;
  cursor: pointer;
}
/* ================= LUXURY REPORT CONTAINER ================= */

.report-container {
  margin-top: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Taller Vertical Card Like Login */
.report-box {
  width: 540px;
  min-height: 460px;              /* taller */
  padding: 70px 55px;             /* more vertical spacing */

  border-radius: 30px;

  background: linear-gradient(
    145deg,
    rgba(255,255,255,0.12),
    rgba(255,255,255,0.05)
  );

  backdrop-filter: blur(16px);

  box-shadow:
    0 0 0 2px rgba(127,220,255,0.25),
    0 30px 70px rgba(0,0,0,0.5);

  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 40px;                      /* more spacing */
  align-items: center;
}


/* ================= PREMIUM INDUSTRIAL BUTTON ================= */

.report-btn {
  width: 100%;
  padding: 26px 30px;

  font-size: 18px;
  font-weight: 700;
  letter-spacing: 1px;

  border-radius: 20px;
  border: none;
  cursor: pointer;

  background: linear-gradient(
    145deg,
    #4a5f6b,
    #344954
  );

  color: #e6f7fb;

  box-shadow:
    inset 0 0 0 2px rgba(127,220,255,0.35),
    0 12px 28px rgba(0,0,0,0.45);

  transition: all 0.3s ease;
}


/* ================= HOVER ================= */

.report-btn:hover {
  transform: translateY(-5px);

  background: linear-gradient(
    145deg,
    #5f7886,
    #425c68
  );

  box-shadow:
    inset 0 0 0 2px rgba(127,220,255,0.6),
    0 18px 35px rgba(0,0,0,0.55),
    0 0 25px rgba(127,220,255,0.3);
}


/* ================= ACTIVE ================= */

.report-btn:active {
  transform: translateY(0);

  box-shadow:
    inset 0 0 0 2px rgba(127,220,255,0.8),
    0 6px 16px rgba(0,0,0,0.45);
}

</style>