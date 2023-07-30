<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',justifyContent:'center',alignItems:'center' }">
                    <div style="text-align: center;height: 100%;width: 40%">
                        <p style="font-size: 3rem;font-weight: 700;">KineticHub</p>
                        <a-form
                            :form="form"
                            @submit="handleSubmit"
                        >
                            <a-form-item>
                                <a-input
                                    v-decorator="[
                                      'query',
                                      { rules: [{ required: true, message: 'Please input your query!' }] },
                                    ]"
                                    placeholder="..."
                                >
                                    <a-icon slot="prefix" type="search" />
                                    <a-button slot="suffix" type="primary" html-type="submit">
                                        Search
                                    </a-button>
                                </a-input>
                            </a-form-item>
                            <a-form-item>
                                Search reations by:
                                <a-radio-group
                                    v-decorator="[
                                      'type',
                                      { rules: [{ required: true, message: 'Please select a search type!' }] },
                                    ]"
                                >
                                    <a-radio-button value="ec_number">
                                        EC number
                                    </a-radio-button>
                                    <a-radio-button value="name">
                                        Name
                                    </a-radio-button>
                                    <a-radio-button value="type">
                                        Type
                                    </a-radio-button>
                                    <a-radio-button value="substrate">
                                        Substrate
                                    </a-radio-button>
                                    <a-radio-button value="product">
                                        Product
                                    </a-radio-button>
                                </a-radio-group>
                            </a-form-item>
                        </a-form>
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
import sidebar from "@/components/sidebar.vue";
export default {
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'search' });
    },
    components:{
        sidebar
    },
    data() {
        return {
            defaultActivate:"['1']",
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
        async handleSubmit(e) {
            e.preventDefault();
            this.form.validateFields(async (err, values) => {
                if (!err) {
                    localStorage.setItem('searchQuery', values.query);
                    localStorage.setItem('searchType', values.type);
                    console.log('Received values of form: ', values);
                    window.location.href = '/reaction'
                }
            });
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
