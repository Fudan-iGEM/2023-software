<template>
    <a-layout-sider v-model="collapsed" collapsible width="300">
        <div class="logo">
            <p style="font-size: 40px;text-align: center;overflow: hidden">aaaaaaa</p>
        </div>
        <a-menu theme="dark" mode="inline" :default-selected-keys=defaultActivate>
            <a-sub-menu key="sub1">
                <span slot="title"><a-icon type="database" /><span>Step 1: KineticHub</span></span>
                <a-menu-item key="1" @click="toSearch()">
                    <a-icon type="search" />Search Enzyme
                </a-menu-item>
                <a-menu-item key="2">
                    <a-icon type="build" />Build Reactions
                </a-menu-item>
                <a-menu-item key="3" @click="toAddEnzyme()">
                    <a-icon type="plus-circle" />Add Enzyme
                </a-menu-item>
            </a-sub-menu>
            <a-menu-item key="4">
                <a-icon type="compass" />
                <span>Step 2: xxx</span>
            </a-menu-item>
            <a-menu-item key="5">
                <a-icon type="book" />
                <span>Docs</span>
            </a-menu-item>
            <a-menu-item key="6" @click="toWiki()">
                <a-icon type="info-circle" />
                <span>Wiki</span>
            </a-menu-item>
            <a-menu-item key="7" @click="toGitlab()">
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
        toSearch(){
            window.location.href = '/search';
        },
        toAddEnzyme(){
            window.location.href = '/addEnzyme';
        },
        toGitlab(){
            window.open('https://gitlab.igem.org/2023/software-tools/fudan')
        },
        toWiki(){
            window.open('https://2023.igem.wiki/fudan/software')
        },
    },
};
</script>
<style scoped>
.logo {
    height: 50px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px;
}
</style>