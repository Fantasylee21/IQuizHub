<template>
    <div class="body">
        <div class="shell">
            <div class="container a-container" id="a-container">
                <form @submit.prevent="handleSignup" class="form" id="a-form">
                    <h2 class="form_title title">Create Account</h2>
                    <input
                            type="text"
                            class="form_input"
                            placeholder="Username (3-16 letters, numbers, or underscores)"
                            v-model="signupForm.username"
                    />
                    <input
                            type="password"
                            class="form_input"
                            placeholder="Password (6-20 letters, numbers, or characters)"
                            v-model="signupForm.password"
                    />
                    <input
                            type="text"
                            class="form_input"
                            placeholder="Phone (valid phone number)"
                            v-model="signupForm.phone"
                    />
                    <input
                            type="email"
                            class="form_input"
                            placeholder="Email (valid email address)"
                            v-model="signupForm.email"
                    />
                    <button class="form_button button submit">SIGN UP</button>
                </form>
            </div>

            <div class="container b-container" id="b-container">
                <form @submit.prevent="handleLogin" class="form" id="b-form">
                    <h2 class="form_title title">Log In</h2>
                    <input
                            type="text"
                            class="form_input"
                            placeholder="User Name"
                            v-model="loginForm.username"
                    />
                    <input
                            type="password"
                            class="form_input"
                            placeholder="Password"
                            v-model="loginForm.password"
                    />
                    <a class="form_link">Forgot password?</a>
                    <button class="form_button button submit">SIGN IN</button>
                </form>
            </div>

            <div class="switch" id="switch-cnt">
                <div class="switch_circle"></div>
                <div class="switch_circle switch_circle-t"></div>
                <div
                        class="switch_container"
                        id="switch-c1"
                        :class="{ 'is-hidden': isSignInVisible }"
                >
                    <h2 class="switch_title title" style="letter-spacing: 0">Welcome Back！</h2>
                    <p class="switch_description description">
                        Do you already have an account? Go log in to your account and enter the wonderful world!!!
                    </p>
                    <button class="switch_button button switch-btn" @click="changeForm">
                        SIGN UP
                    </button>
                </div>

                <div
                        class="switch_container"
                        id="switch-c2"
                        :class="{ 'is-hidden': !isSignInVisible }"
                >
                    <h2 class="switch_title title" style="letter-spacing: 0">Hello Markers！</h2>
                    <p class="switch_description description">
                        Register an account and become a proud fan member, let's embark on a wonderful journey!
                    </p>
                    <button class="switch_button button switch-btn" @click="changeForm">
                        SIGN IN
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {ElMessage} from 'element-plus'
import UtilMethods from '@/utils/UtilMethod'
import api from "@/api";
import {useProfileStore} from "@/stores/profile";

const isSignInVisible = ref(true)
const profile = useProfileStore()

const signupForm = ref({
    username: '',
    password: '',
    phone: '',
    email: ''
})

const loginForm = ref({
    username: '',
    password: ''
})

const handleSignup = async () => {
    await api.register(signupForm.value)
}

const handleLogin = async () => {
    const ret = await api.login(loginForm.value)
    if (ret) {
        ElMessage.success('successfully logged in!')
        profile.updateProfile(ret)
        localStorage.setItem('id', profile.id)
        UtilMethods.jump('/staging')
    } else {
        ElMessage.error('login failed!')
    }
}

const validateSignupForm = () => {
    const usernamePattern = /^[a-zA-Z0-9_]{3,16}$/
    const passwordPattern = /^[a-zA-Z0-9!@#$%^&*]{6,20}$/
    const phonePattern = /^[1-9]\d{9,14}$/
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/

    if (!usernamePattern.test(signupForm.value.username)) {
        ElMessage.error('用户名格式不正确')
        return false
    }
    if (!passwordPattern.test(signupForm.value.password)) {
        ElMessage.error('密码格式不正确')
        return false
    }
    if (!phonePattern.test(signupForm.value.phone)) {
        ElMessage.error('手机号格式不正确')
        return false
    }
    if (!emailPattern.test(signupForm.value.email)) {
        ElMessage.error('邮箱格式不正确')
        return false
    }
    return true
}

const changeForm = () => {
    const switchCtn: any = document.querySelector('#switch-cnt')
    const switchCircle: any = document.querySelectorAll('.switch_circle')
    const switchC1: any = document.querySelector('#switch-c1')
    const switchC2: any = document.querySelector('#switch-c2')
    const aContainer: any = document.querySelector('#a-container')
    const bContainer: any = document.querySelector('#b-container')

    switchCtn.classList.add('is-gx')
    setTimeout(() => {
        switchCtn.classList.remove('is-gx')
    }, 1500)
    switchCtn.classList.toggle('is-txr')
    switchCircle[0].classList.toggle('is-txr')
    switchCircle[1].classList.toggle('is-txr')

    switchC1.classList.toggle('is-hidden')
    switchC2.classList.toggle('is-hidden')
    aContainer.classList.toggle('is-txl')
    bContainer.classList.toggle('is-txl')
    bContainer.classList.toggle('is-z')

    isSignInVisible.value = !isSignInVisible.value
}
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    /* 字体无法选中 */
    user-select: none;
}

.body {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    color: #a0a5a8;
    background: linear-gradient(to bottom, #2980b9, #6dd5fa, #ffffff);
}

.shell {
    position: relative;
    width: 1000px;
    min-width: 1000px;
    min-height: 600px;
    height: 600px;
    padding: 25px;
    background-color: rgba(236, 240, 243, 0.8);
    border-radius: 12px;
    overflow: hidden;
}

/* 设置响应式 */
@media (max-width: 1200px) {
    .shell {
        transform: scale(0.7);
    }
}

@media (max-width: 1000px) {
    .shell {
        transform: scale(0.6);
    }
}

@media (max-width: 800px) {
    .shell {
        transform: scale(0.5);
    }
}

@media (max-width: 600px) {
    .shell {
        transform: scale(0.4);
    }
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    width: 600px;
    height: 100%;
    padding: 25px;
    background-color: #ecf0f3;
    transition: 1.25s;
}

.form {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.iconfont {
    margin: 0 5px;
    border: rgba(0, 0, 0, 0.5) 2px solid;
    border-radius: 50%;
    font-size: 25px;
    padding: 3px;
    opacity: 0.5;
    transition: 0.1s;
}

.iconfont:hover {
    opacity: 1;
    transition: 0.15s;
    cursor: pointer;
}

.form_input {
    width: 350px;
    height: 40px;
    margin: 4px 0;
    padding-left: 25px;
    font-size: 13px;
    letter-spacing: 0.15px;
    border: none;
    outline: none;
    background-color: #ecf0f3;
    transition: 0.25s ease;
    border-radius: 8px;
    box-shadow: inset 2px 2px 4px #d1d9e6,
    inset -2px -2px 4px #f9f9f9;
}

.form_input:focus {
    box-shadow: inset 4px 4px 4px #d1d9e6,
    inset -4px -4px 4px #f9f9f9;
}

.form_span {
    margin-top: 30px;
    margin-bottom: 12px;
}

.form_link {
    color: #181818;
    font-size: 15px;
    margin-top: 25px;
    border-bottom: 1px solid #a0a5a8;
    line-height: 2;
}

.title {
    font-size: 34px;
    font-weight: 700;
    line-height: 3;
    color: #181818;
    letter-spacing: 10px;
}

.description {
    font-size: 14px;
    letter-spacing: 0.25px;
    text-align: center;
    line-height: 1.6;
}

.button {
    width: 180px;
    height: 50px;
    border-radius: 25px;
    margin-top: 50px;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 1.15px;
    background-color: #4b70e2;
    color: #f9f9f9;
    box-shadow: 8px 8px 16px #d1d9e6,
    -8px -8px 16px #f9f9f9;
    border: none;
    outline: none;
}

.a-container {
    z-index: 100;
    left: calc(100% - 600px);
}

.b-container {
    left: calc(100% - 600px);
    z-index: 0;
}

.switch {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 400px;
    padding: 50px;
    z-index: 200;
    transition: 1.25s;
    background-color: #ecf0f3;
    overflow: hidden;
    box-shadow: 4px 4px 10px #d1d9e6,
    -4px -4px 10px #d1d9e6;
}

.switch_circle {
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background-color: #ecf0f3;
    box-shadow: inset 8px 8px 12px #b8bec7,
    inset -8px -8px 12px #fff;
    bottom: -60%;
    left: -60%;
    transition: 1.25s;
}

.switch_circle-t {
    top: -30%;
    left: 60%;
    width: 300px;
    height: 300px;
}

.switch_container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: absolute;
    width: 400px;
    padding: 50px 55px;
    transition: 1.25s;
}

.switch_button {
    cursor: pointer;
}

.submit {
    cursor: pointer;
}

.switch_button:hover,
.submit:hover {
    box-shadow: 6px 6px 10px #d1d9e6,
    -6px -6px 10px #f9f9f9;
    transform: scale(0.985);
    transition: 0.25s;
}

.switch_button:active,
.switch_button:focus {
    box-shadow: 2px 2px 6px #d1d9e6,
    -2px -2px 6px #f9f9f9;
    transform: scale(0.97);
    transition: 0.25s;
}

.is-txr {
    left: calc(100% - 400px);
    transition: 1.25s;
    transform-origin: left;
}

.is-txl {
    left: 0;
    transition: 1.25s;
    transform-origin: right;
}

.is-z {
    z-index: 200;
    transition: 1.25s;
}

.is-hidden {
    visibility: hidden;
    opacity: 0;
    position: absolute;
    transition: 1.25s;
}

.is-gx {
    animation: is-gx 1.25s;
}

@keyframes is-gx {
    0%,
    10%,
    100% {
        width: 400px;
    }

    30%,
    50% {
        width: 500px;
    }
}

.form_title {
    font-size: 34px;
    font-weight: 700;
    line-height: 3;
    color: #181818;
    letter-spacing: 0px;
}
</style>