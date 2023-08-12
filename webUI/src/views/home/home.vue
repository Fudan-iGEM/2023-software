<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',justifyContent:'center',alignItems:'center' }">
                    <div style="text-align: center;height: 100%">
                        <img :src="require('@/assets/img/logo.svg')" style="height: 20rem">
                        <p style="font-size: 3rem;font-weight: 700;">Welcome to RAP!</p>
                        <p style="font-size: 1rem">You can start building your linear reactions from step 1.</p>
                        <p style="font-size: 1rem">And then run step 2 to build your pRAP system.</p>
                        <p style="font-size: 1rem">You can also promote your own pRAP system design after a DBTL cycle using pRAPer.</p>
                        <p style="font-size: 1rem;font-weight: 700;">For more tutorials and details, please visit our documentation and our wiki!</p>
                    </div>
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                RAP ©2023 Created by mistyfield
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import sidebar from '@/components/sidebar.vue'
export default {
    components:{
        sidebar
    },
    created() {
        this.$notification.open({
            message: '🤝 Seek for collaboration!',
            description:
                'If your team needs to use multiple enzyme coupling to participate in a module, we welcome the opportunity to collaborate with you and offer you help with wet and dry lab, and we are in desire of your feedback and comment on RAP!',
            icon: <a-icon type="smile" style="color: #e37654" />,
            btn: h => {
                return h(
                    'a-button',
                    {
                        props: {
                            type: 'primary',
                            size: 'small',
                        },
                        on: {
                            click: () => window.location.href = '/comment',
                        },
                    },
                    'Leave a comment',
                );
                },
            duration:null
        });
    },
    data() {
        return {
            defaultActivate:['1'],
        };
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
