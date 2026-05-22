// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://101.101.101.50:5000"
// });

// api.interceptors.request.use(config => {
//   const token = localStorage.getItem("token");
//   if (token) config.headers.Authorization = `Bearer ${token}`;
//   return config;
// });

// export default api;


import axios from "axios";

const api = axios.create({
  baseURL: "https://api.appvirtualex.com"
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;