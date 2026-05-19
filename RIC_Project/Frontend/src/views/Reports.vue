<template>
  <div class="app">
    <Sidebar />

    <main class="main">
      <Header />

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

      
    </main>
  </div>
</template>


<script>
import Header from '../components/Header.vue';
import Sidebar from '../components/Sidebar.vue';

export default {
  name: "Reports",
  components: { Sidebar, Header },
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
  background: rgba(0, 0, 0, 0.18);
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