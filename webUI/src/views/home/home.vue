<template>
  <p>1234s</p>
</template>

<script>
import axios from "axios";

export default {
    name: "home",
    created() {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/login';
        }
        else {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
        axios.get('/api/protected')
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.error(error);
                window.location.href = '/login';
            });
    }
};
</script>
<style scoped>

</style>