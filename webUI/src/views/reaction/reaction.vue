<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',flexDirection:'column',justifyContent:'flex-start',alignItems:'center' }"
                >
                    <div style="text-align: center;height: 100%;padding-bottom: 3rem">
                        <a-form
                            layout="inline"
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
                                    <a-radio-button value="substrates">
                                        Substrate
                                    </a-radio-button>
                                    <a-radio-button value="products">
                                        Product
                                    </a-radio-button>
                                </a-radio-group>
                            </a-form-item>
                        </a-form>
                </div>
                <a-table
                    :columns="columns"
                    :data-source="data"
                    :scroll="{ x: 1500, y: 600 }"
                    style="width: 95%"
                >
                    <p slot="title" style="font-weight: 700;font-size: 1rem">
                        Your Search result of {{searchQuery}} on {{typeDict[searchType]}}:
                    </p>
                    <a slot="action">action</a>
                </a-table>
            </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                pRAPer ©2023 Created by mistyfield
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import axios from 'axios';
import sidebar from "@/components/sidebar.vue";
const columns = [
    { title: 'EC number', width: 100, dataIndex: 'ec_number', key: 'ec_number', fixed: 'left' },
    { title: 'EC annotation', width: 200, dataIndex: 'ec_annotation', key: 'ec_annotation', fixed: 'left' },
    { title: 'Name', dataIndex: 'name', key: 'name', width: 250},
    { title: 'Systematic name', dataIndex: 'systematic_name', key: 'systematic_name', width: 250 },
    { title: 'Type', dataIndex: 'type', key: 'type', width: 200 },
    { title: 'Formula', dataIndex: 'str', key: 'str', width: 300 },
    {
        title: 'Action',
        key: 'operation',
        fixed: 'right',
        scopedSlots: { customRender: 'action' },
    },
];
const data = []
export default {
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'search' });
    },
    created() {
        const searchType = localStorage.getItem('searchType');
        const searchQuery = localStorage.getItem('searchQuery');
        if (!searchType || !searchQuery) {
            window.location.href = '/search';
        }
        axios.post('/api/search/reaction', {
            'searchType': searchType,
            'searchQuery':searchQuery})
            .then(response => {
                this.data = response.data})
            .catch(error => {
                console.error(error);
            });
    },
    components:{
        sidebar
    },
    data() {
        return {
            defaultActivate: "['2']",
            searchResults: [],
            data,
            columns,
            searchType: localStorage.getItem('searchType'),
            searchQuery: localStorage.getItem('searchQuery'),
            typeDict:{
                'ec_number': 'EC number',
                'name': 'Name',
                'type': 'Type',
                'substrates': 'Substrate',
                'products': 'Products'
            },
        };
    },
    methods: {
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
