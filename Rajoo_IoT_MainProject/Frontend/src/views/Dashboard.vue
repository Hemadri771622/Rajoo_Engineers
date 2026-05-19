<template>
  <div class="login-wrapper">
    <!-- Background Video -->
    <video
      class="bg-video"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
    >
      <source src="/bg.mp4" type="video/mp4" />
    </video>

    <!-- Dark Overlay -->
    <div class="overlay"></div>

    <!-- Top Bar -->
    <header class="top-bar">
      <img src="/rajoo_logo.png" class="rajoo-logo" />

      <div class="clock-box">
        <div class="date">{{ date }}</div>
        <div class="time">{{ time }}</div>
      </div>
    </header>

    <h1 class="title">THREE LAYER BLOWN FILM LINE</h1>

    <div class="login-card">
      <img src="/user-icon.png" class="profile-icon" />

      <select v-model="role" class="input">
        <option>Operator</option>
        <option>Admin</option>
        <option>Guest</option>
      </select>

      <input
        type="password"
        v-model="password"
        class="input"
        placeholder="Password"
        readonly
        @focus="removeReadonly"
      />

      <button class="login-btn" @click="login">
        LOG IN
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <footer class="footer">
      MODEL :- RFCF-2550-40-1800
    </footer>
  </div>
</template>

<script>
export default {
  name: "Login",

  data() {
    return {
      role: "Operator",
      password: "",
      error: "",
      time: "",
      date: "",
      clockTimer: null
    };
  },

  mounted() {
    this.updateClock();
    this.clockTimer = setInterval(this.updateClock, 1000);
  },

  beforeUnmount() {
    clearInterval(this.clockTimer);
  },

  methods: {
    updateClock() {
      const now = new Date();
      this.time = now
        .toLocaleTimeString("en-IN", {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: true
        })
        .toUpperCase();

      this.date = now.toLocaleDateString("en-IN");
    },

    removeReadonly(event) {
      event.target.removeAttribute("readonly");
    },

    async login() {
      this.error = "";

      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/auth/login",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              role: this.role,
              password: this.password.trim()
            })
          }
        );

        if (!response.ok) {
          this.error = "Invalid credentials";
          return;
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);

        this.$router.push("/dashboard");
      } catch (error) {
        this.error = "Server error";
      }
    }
  }
};
</script>

<style>
.login-wrapper {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: "Segoe UI", sans-serif;
  color: #e6f6ff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Background video */
.bg-video {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  z-index: -2;
}

/* Overlay */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(3, 20, 35, 0.85);
  z-index: -1;
}

/* Top bar */
.top-bar {
  position: absolute;
  top: 18px;
  left: 30px;
  right: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rajoo-logo {
  height: 46px;
}

.clock-box {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 18px;
  border-radius: 14px;
  backdrop-filter: blur(10px);
  text-align: center;
}

/* Title */
.title {
  margin-top: 140px;
  font-size: 44px;
  letter-spacing: 5px;
  font-weight: 800;
  color: #a8ecff;
}

/* Login card */
.login-card {
  width: 400px;
  min-height: 620px; /* ⬅ minimum height */
  padding: 54px 44px;
  margin-top: 60px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 22px;
  backdrop-filter: blur(14px);
  text-align: center;
}


.profile-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 40px;
}

.input {
  width: 90%;
  padding: 14px;
  margin-bottom: 30px;
  border-radius: 12px;
  border: none;
  background: rgba(0, 0, 0, 0.45);
  color: #ffffff;
  outline: none;
}

/* Button */
.login-btn {
  width: 50%;
  padding: 14px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  font-weight: 700;
  cursor: pointer;
}

/* Error */
.error {
  margin-top: 10px;
  color: #ff6b6b;
}

/* Footer */
.footer {
  position: absolute;
  bottom: 18px;
  width: 100%;
  text-align: center;
  font-size: 18px;
  letter-spacing: 2px;
  font-weight: 600;
  color: #c6f2ff;
}
</style>
