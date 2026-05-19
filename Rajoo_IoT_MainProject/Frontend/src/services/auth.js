import api from "./api";

export async function login(username, password) {
  const res = await api.post("/api/auth/login", { username, password });
  localStorage.setItem("token", res.data.access_token);
  localStorage.setItem("role", res.data.role);
}
