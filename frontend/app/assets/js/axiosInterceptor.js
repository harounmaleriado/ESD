// Axios interceptor
axios.interceptors.request.use(async function(config) {
    
    const token = sessionStorage.getItem('idToken');
    console.log("Interceptor called, Token:");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        console.log("Token added to Authorisation header");
    }
    return config;
}, function(error) {
    return Promise.reject(error);
});
