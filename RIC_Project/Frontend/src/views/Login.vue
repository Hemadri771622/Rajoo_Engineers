<template>
  <div class="login-wrapper">

    <!-- Background video -->
    <video autoplay muted loop playsinline class="bg-video">
      <source src="/bg.mp4" type="video/mp4" />
    </video>

    <div class="overlay"></div>

    <!-- Top bar -->
    <header class="top-bar">

      <!-- LEFT -->
      <img src="/VirtualEX_logo.png" class="VirtualEX-logo" />

      <!-- RIGHT -->
      <div class="rajoo-right-logo">
        <img src="/rajoo_logo.png" alt="Rajoo Logo" />
      </div>

    </header>

    <!-- Title -->
    <h2 class="title">THREE LAYER BLOWN FILM LINE</h2>

    <!-- Login card -->
    <div class="login-card">

      <img src="/user-icon.png" class="profile-icon" />

      <select v-model="role" class="input">
        <option>Operator</option>
        <option>Admin</option>
        <option>Guest</option>
      </select>

      <!-- PASSWORD -->
      <div class="password-wrapper">

        <input
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          placeholder="Password"
          class="input password-input"
        />

        <span
          class="eye material-icons"
          @click="showPassword = !showPassword"
        >
          {{ showPassword ? 'visibility' : 'visibility_off' }}
        </span>

      </div>

      <button class="login-btn" @click="login">
        LOG IN
      </button>

      <p v-if="error" class="error">
        {{ error }}
      </p>

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
      error: ""
    };
  },

  methods: {

    async login() {

      this.error = "";

      try {

        const res = await fetch(
          "http://127.0.0.1:5000/api/auth/login",
          {
            method: "POST",

            headers: {
              "Content-Type": "application/json"
            },

            body: JSON.stringify({
              role: this.role,
              password: this.password.trim()
            })
          }
        );

        const text = await res.text();

        let data = {};

        try {
          data = JSON.parse(text);
        } catch {
          console.error("Non-JSON response:", text);
        }

        if (!res.ok) {
          this.error =
            data.message || "Invalid credentials";
          return;
        }

        localStorage.setItem(
          "token",
          data.access_token
        );

        localStorage.setItem(
          "role",
          data.role
        );

        this.$router.push("/dashboard");

      } catch (err) {

        console.error("LOGIN ERROR:", err);

        this.error =
          "Server not reachable (CORS / Network error)";
      }
    }
  }
};
</script>

<style scoped>
.login-wrapper {
  height: 100vh;

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

  background: rgba(3, 20, 35, 0.68);

  z-index: -1;
}

/* TOP BAR */
.top-bar {
  position: absolute;

  top: 18px;
  left: 30px;
  right: 30px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* VIRTUALEX */
.VirtualEX-logo {
  height: 86px;
  width: 180px;

  padding: 4px 6px;

  border-radius: 18px;

  background: rgba(255, 255, 255, 0.10);

  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);

  border: 1px solid rgba(255,255,255,0.14);

  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.10),
    0 4px 14px rgba(0,0,0,0.28);

  object-fit: cover;

  display: block;
}

/* RIGHT RAJOO */
.rajoo-right-logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.rajoo-right-logo img {
  width: 180px;
  height: auto;

  padding: 8px 18px;

  border-radius: 18px;

  background: rgba(255, 255, 255, 0.10);

  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);

  border: 1px solid rgba(255,255,255,0.14);

  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.10),
    0 4px 14px rgba(0,0,0,0.28);

  object-fit: contain;

  display: block;
}

/* TITLE */
.title {
  margin-top: 150px;

  text-align: center;

  font-size: 44px;

  letter-spacing: 5px;

  font-weight: 800;

  color: #a8ecff;

  text-transform: uppercase;

  text-shadow:
    0 0 12px rgba(0, 180, 255, 0.4),
    0 0 24px rgba(0, 180, 255, 0.2);
}

/* LOGIN CARD */
.login-card {
  width: 400px;

  padding: 44px;

  margin: 40px auto 0;

  background: rgba(255, 255, 255, 0.10);

  border-radius: 22px;

  backdrop-filter: blur(14px);

  border: 1px solid rgba(255,255,255,0.10);

  text-align: center;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.35);
}

/* USER ICON */
.profile-icon {
  width: 120px;
  height: 120px;

  margin-bottom: 40px;
}

/* INPUTS */
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

/* PASSWORD */
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

/* LOGIN BUTTON */
.login-btn {
  width: 50%;

  padding: 14px;

  margin: 10px auto 0;

  display: block;

  border-radius: 14px;

  border: none;

  background:
    linear-gradient(
      135deg,
      #4facfe,
      #00f2fe
    );

  font-weight: 700;

  cursor: pointer;
}

/* ERROR */
.error {
  color: #ff6b6b;

  margin-top: 14px;
}
</style>