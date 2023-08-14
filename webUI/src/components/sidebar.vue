<template>
    <a-layout-sider v-model="collapsed" collapsible width="300">
        <div class="logo">
            <img :src="require('@/assets/img/logo.svg')"><p>RAP</p>
        </div>
        <a-menu theme="dark" mode="inline" :default-selected-keys=defaultActivate>
            <a-menu-item key="1" @click="toHome()">
                <a-icon type="home" />
                <span>Home</span>
            </a-menu-item>
            <a-sub-menu key="sub1">
                <span slot="title"><a-icon type="database" /><span>Step 1: KineticHub</span></span>
                <a-menu-item key="2" @click="toSearch()">
                    <a-icon type="search" />Search Enzyme
                </a-menu-item>
                <a-menu-item key="3" @click="toBuild()">
                    <a-icon type="build" />Build Reactions
                </a-menu-item>
                <a-menu-item key="4" @click="toAddEnzyme()">
                    <a-icon type="plus-circle" />Add Enzyme
                </a-menu-item>
            </a-sub-menu>
            <a-menu-item key="5">
                <a-icon type="compass" />
                <span>Step 2: pRAP Builder (In progress)</span>
            </a-menu-item>
            <a-menu-item key="6" @click="toDocs()">
                <a-icon type="book" />
                <span>Docs</span>
            </a-menu-item>
            <a-menu-item key="7" @click="toWiki()">
                <a-icon type="info-circle" />
                <span>Wiki</span>
            </a-menu-item>
            <a-menu-item key="8" @click="toComment()">
                <a-icon type="edit" />
                <span>Leave a comment</span>
            </a-menu-item>
            <a-menu-item key="9" @click="toGitlab()">
                <a-icon type="gitlab" />
                <span>Gitlab</span>
            </a-menu-item>
        </a-menu>
    </a-layout-sider>
</template>
<script>
export default {
    data() {
        return {
            collapsed: false,
        };
    },
    props:['defaultActivate'],
    methods:{
        toHome(){
            window.location.href = '/home';
        },
        toSearch(){
            window.location.href = '/search';
        },
        toAddEnzyme(){
            window.location.href = '/addEnzyme';
        },
        toGitlab(){
            window.open('https://gitlab.igem.org/2023/software-tools/fudan');
        },
        toWiki(){
            window.open('https://2023.igem.wiki/fudan/software');
        },
        toComment(){
            window.location.href = '/comment';
        },
        toBuild() {
            window.location.href = '/buildReactions';
        },
        toDocs(){
            window.open('https://mistyfield.github.io/RAP-Docs/');
        }
    },
};
</script>
<style scoped>
.logo {
    height: 80px;
    background: rgba(255, 255, 255, 0.2);
    display: inline-flex;
    overflow: hidden;
    align-items: center;
    width: 100%;
}
.logo img{
    max-height: 100%;
    padding-right: 10px;
}
.logo p{
    font-size: 60px;
    color: rgb(255, 246, 240);
    margin: 0;
}
</style>