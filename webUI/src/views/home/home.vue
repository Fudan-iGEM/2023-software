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
                <a-drawer
                    title="Privacy Policy"
                    placement="bottom"
                    :closable="false"
                    :visible="drawerVisible"
                    @close="onClose"
                    height="200px"
                    class="bottom-drawer"
                >
                    <p style="display: inline-block">This website uses cookies to ensure you get the best experience on our website.</p>
                    <div style="display: inline-block;position: absolute;right: 1rem">
                        <a-button type="primary" class="drawer-btn" @click="showPrivacy">
                            Learn More About Privacy Policies
                        </a-button>
                        <a-button type="primary" @click="onClose">
                            Allow
                        </a-button>
                    </div>
                    <a-drawer
                        title="Privacy Policy of RAP"
                        placement="bottom"
                        height="600px"
                        :closable="true"
                        :visible="privacyDrawer"
                        @close="onPrivacyDrawerClose"
                    >
                        <p>This page is used to inform website visitors regarding our policies with the collection, use, and disclosure of Personal Information if anyone decided to use our Service, the RAP website.</p>
                        <p>If you choose to use our Service, then you agree to the collection and use of information in relation with this policy. The Personal Information that we collect are used for providing and improving the Service. We will not use or share your information with anyone except as described in this Privacy Policy.</p>
                        <h2>Cookies</h2>
                        <p>Cookies are files with small amount of data that is commonly used an anonymous unique identifier. These are sent to your browser from the website that you visit and are stored on your computer's hard drive.</p>
                        <p>Our website uses these “cookies” to collection information and to improve our Service. You have the option to either accept or refuse these cookies, and know when a cookie is being sent to your computer. If you choose to refuse our cookies, you may not be able to use some portions of our Service.</p>
                        <h2>Data Privacy</h2>
                        <p>Data submitted in RAP is only used for computation, we don't collect sequences, but data submitted to KineticHub is viewed as public.</p>
                        <h2>Changes to This Privacy Policy</h2>
                        <p>We may update our Privacy Policy from time to time. Thus, we advise you to review this page periodically for any changes. We will notify you of any changes by posting the new Privacy Policy on this page. These changes are effective immediately, after they are posted on this page.</p>
                        <h2>Contact Us</h2>
                        <p>If you have any questions or suggestions about our Privacy Policy, do not hesitate to <a href="mailto:20301050198@fudan.edu.cn">contact us</a>.</p>
                    </a-drawer>
                </a-drawer>
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
            drawerVisible:true,
            privacyDrawer:false,
        };
    },
    methods:{
        onClose() {
            this.drawerVisible = false;
        },
        showPrivacy(){
            this.privacyDrawer = true;
        },
        onPrivacyDrawerClose(){
            this.privacyDrawer = false;
        }
    }
};
</script>

<style>
#app{
    font-family: HarmonyOS_Sans, Helvetica, Arial, sans-serif;
    font-weight: 500;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
.drawer-btn{
    margin-left: 1rem;
    margin-right: 1rem;
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
