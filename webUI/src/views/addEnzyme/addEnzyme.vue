<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout-sider v-model="collapsed" collapsible width="300">
            <div class="logo">
                <p style="font-size: 40px;text-align: center;overflow: hidden">aaaaaaa</p>
            </div>
            <a-menu theme="dark" mode="inline" :default-selected-keys="['3']">
                <a-sub-menu key="sub1">
                    <span slot="title"><a-icon type="database" /><span>Step 1: KineticHub</span></span>
                    <a-menu-item key="1" @click="toSearch()">
                        <a-icon type="search" />Search Enzyme
                    </a-menu-item>
                    <a-menu-item key="2">
                        <a-icon type="build" />Build Reactions
                    </a-menu-item>
                    <a-menu-item key="3">
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
        <a-layout>
            <a-layout-content style="margin: 0">
                <div :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',justifyContent:'center',alignItems:'center' }">
                    <div style="text-align: center;height: 100%">
                        <p style="font-size: 3rem;font-weight: 700;">Welcome to pRAPer!</p>
                        <p style="font-size: 1rem">You can start building your linear reactions from step 1.</p>
                        <p style="font-size: 1rem">And then run step 2 to build your pRAP system.</p>
                        <p style="font-size: 1rem">You can also promote your own pRAP system design after a DBTL cycle using pRAPer.</p>
                        <p style="font-size: 1rem"><strong>For more tutorials and details, please visit our documentation and our wiki!</strong></p>
                    </div>
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                pRAPer ©2023 Created by mistyfield
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
export default {
    data() {
        return {
            collapsed: false,
        };
    },
    methods:{
        toSearch(){
            window.location.href = '/search';
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

<style>
#app{
    font-family: HarmonyOS_Sans, Helvetica, Arial, sans-serif;
    font-weight: 500;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
#app .logo {
    height: 50px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px;
}
::-webkit-scrollbar{
    width: 5px;
    height: 5px;
}

::-webkit-scrollbar-thumb:vertical{
    height: 5px;
    background-color: #e37654;
}
::-webkit-scrollbar-thumb:horizontal{
    width: 5px;
    background-color: #e37654;
}
</style>
