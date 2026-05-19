<template>
  <div class="login-wrapper">
    <!-- Background video -->
    <video autoplay muted loop playsinline class="bg-video">
      <source src="/bg.mp4" type="video/mp4" />
    </video>

    <div class="overlay"></div>

    <!-- Top bar -->
    <header class="top-bar">
      <img src="/rajoo_logo.png" class="rajoo-logo" />

      <div class="clock-box">
        <div class="date">{{ date }}</div>
        <div class="time">{{ time }}</div>
      </div>
    </header>

    <!-- Title -->
    <h1 class="title">THREE LAYER BLOWN FILM LINE</h1>

    <!-- Login card -->
    <div class="login-card">
      <img src="/user-icon.png" class="profile-icon" />

      <select v-model="role" class="input">
        <option>Operator</option>
        <option>Admin</option>
        <option>Guest</option>
      </select>

      <!-- PASSWORD WITH EYE (ADDED, UI SAME) -->
      <div class="password-wrapper">
        <input
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          placeholder="Password"
          class="input password-input"
        />
        <span class="eye material-icons" @click="showPassword = !showPassword">
          {{ showPassword ? 'visibility' : 'visibility_off' }}
        </span>
      </div>

      <button class="login-btn" @click="login">LOG IN</button>

      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <div class="footer">
      MODEL :- RFCF-2550-40-1800
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      role: "Operator",
      password: "",
      showPassword: false,
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

    async login() {
      this.error = "";

      try {
        const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role: this.role,
            password: this.password.trim()
          })
        });

        const text = await res.text();
        let data = {};

        try {
          data = JSON.parse(text);
        } catch {
          console.error("Non-JSON response:", text);
        }

        if (!res.ok) {
          this.error = data.message || "Invalid credentials";
          return;
        }

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);

        this.$router.push("/dashboard");
      } catch (err) {
        console.error("LOGIN ERROR:", err);
        this.error = "Server not reachable (CORS / Network error)";
      }
    }
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  font-family: "Segoe UI", sans-serif;
  color: #e6f6ff;
  z-index: 0;
}

/* Background video */
.bg-video {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  z-index: -1;
}

/* Overlay */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(3, 20, 35, 0.65);
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

/* Clock */
.clock-box {
  background: rgba(255, 255, 255, 0.1);
  padding: 12px 18px;
  border-radius: 14px;
  backdrop-filter: blur(10px);
  text-align: center;
}

.clock-box .date {
  font-size: 18px;
  font-weight: bold;
  opacity: 0.85;
}

.clock-box .time {
  font-size: 18px;
  font-weight: bold;
  opacity: 0.85;
}

/* Title */
.title {
  margin-top: 120px;
  text-align: center;
  font-size: 44px;
  letter-spacing: 5px;
  font-weight: 800;
  color: #a8ecff;
  text-transform: uppercase;
  text-shadow: 0 0 12px rgba(0, 180, 255, 0.4),
               0 0 24px rgba(0, 180, 255, 0.2);
}

/* Login card */
.login-card {
  width: 400px;
  height: 100%;
  padding: 44px;
  margin: 40px auto 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 22px;
  backdrop-filter: blur(14px);
  text-align: center;
}

.profile-icon {
  width: 120px;
  height:120px;
  margin-bottom: 40px;
}

/* Inputs */
.input {
  width: 90%;
  box-sizing: border-box;
  padding: 14px;
  margin-bottom: 30px;
  border-radius: 12px;
  border: none;
  outline: none;
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  font-size: 15px;
}

/* Login button */
.login-btn {
  width: 50%;
  padding: 14px;
  margin: 10px auto 0px;
  display: block;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  font-weight: 700;
  cursor: pointer;
}

/* Error */
.error {
  color: #ff6b6b;
  margin-top: 14px;
}

/* Footer */
.footer {
  position: absolute;
  bottom: 10px;
  width: 100%;
  text-align: center;
  font-size: 18px;
  letter-spacing: 2px;
  font-weight: 600;
  opacity: 0.9;
  color: #c6f2ff;
}

/* ======== ONLY ADDITIONS BELOW (EYE ICON) ======== */

.password-wrapper {
  position: relative;
  width: 90%;
  margin: 0 auto;
}

.password-input {
  width: 100%;
}

.eye {
  position: absolute;
  right: 10px;
  top: 30%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 18px;
  opacity: 0.8;
}
</style>
