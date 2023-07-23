<template>
  <div id="login">
      <div class="login-box">
          <a-form
            id="components-form-login"
            :form="form"
            class="login-form"
            @submit="handleSubmit"
          >
            <h1>Login</h1>
            <a-form-item>
              <a-input
                v-decorator="['userName',{ rules: [{ required: true, message: 'Please input your username!' }] },]"
                placeholder="Username"
              >
                <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)" />
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input-password
                v-decorator="['password',{ rules: [{ required: true, message: 'Please input your Password!' }] },]"
                placeholder="input password"
              >
                <a-icon slot="prefix" type="lock" style="color: rgba(0,0,0,.25)" />
              </a-input-password>
            </a-form-item>
              <a-button type="primary" html-type="submit" class="login-form-button">Log in</a-button>
          </a-form>
      <div class="register">
          <p>
            <i>
              If you don't have an account, you can log in with a public account or by sending an email to
              <a href="mailto:20301050198@fudan.edu.cn">register!</a>
            </i>
          </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
    name: "login",
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'normal_login' });
    },
    methods: {
        handleSubmit(e) {
            e.preventDefault();
            this.form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    axios.post('/api/login', values)
                        .then(response => {
                            console.log(response.data);
                            localStorage.setItem('token', response.data['access_token']);
                            window.location.href = '/home';
                        })
                        .catch(error => {
                            console.error(error);
                        });
                }
            });
        },
    },
}
</script>
<style scoped>
#login {
  font-family: Barlow, Helvetica, Arial, sans-serif;
  font-weight: 500;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: url("@/assets/bg.svg") center/cover no-repeat;
}
.login-box {
    max-width: 60%;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #ffffff88;
    border-radius: 0.5rem;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}
.login-form {
    max-width: 60%;
    margin-top: 1rem;
}
#components-form-login .login-form-button {
    width: 100%;
}
.register {
    margin: 1rem;
}
a-form-item {
    font-size: 1rem;
}
</style>