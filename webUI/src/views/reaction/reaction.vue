<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',flexDirection:'column',justifyContent:'flex-start',alignItems:'center' }"
                >
                    <div style="text-align: center;height: 100%;padding-bottom: 1.5rem;display: inline-flex;align-items:center;">
                        <a-form
                            layout="inline"
                            :form="form"
                            @submit="handleSubmit"
                        >
                            <a-form-item>
                                <a-input
                                    :defaultValue="searchQuery"
                                    v-decorator="[
                                      'query',
                                      {initialValue: searchQuery, rules: [{ required: true, message: 'Please input your query!' }] },
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
                                    :defaultValue="searchType"
                                    v-decorator="[
                                      'type',
                                      {initialValue: searchType, rules: [{ required: true, message: 'Please select a search type!' }] },
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
                        <a-badge :count="count"><a-icon type="experiment" style="font-size: 20px" @click="toBuild"></a-icon></a-badge>
                </div>
                <a-table
                    :columns="columns"
                    :data-source="data"
                    :scroll="{ x: 1500, y: 600 }"
                    style="width: 95%"
                >
                    <a slot="action" slot-scope="text, record" @click="viewKcat(record.ec_number)">Get Kcat</a>
                </a-table>
                <kcat :ec_number="drawerNumber" :visible="drawerVisible" :data="drawerData" @onClose="handleVisibleChange" @update-reactions="handleAdd"></kcat>
            </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                RAP ©2023 Created by mistyfield
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import axios from 'axios';
import sidebar from "@/components/sidebar.vue";
import kcat from "@/components/kcat.vue";
const columns = [
    { title: 'EC number', width: 100, dataIndex: 'ec_number', key: 'ec_number', fixed: 'left' },
    { title: 'EC annotation', width: 200, dataIndex: 'ec_annotation', key: 'ec_annotation', fixed: 'left' },
    { title: 'Name', dataIndex: 'name', key: 'name', width: 250, sorter: (a, b) => a.name.charCodeAt(0) - b.name.charCodeAt(0)},
    { title: 'Systematic name', dataIndex: 'systematic_name', key: 'systematic_name', width: 250 },
    { title: 'Type', dataIndex: 'type', key: 'type', width: 200 },
    { title: 'Formula', dataIndex: 'str', key: 'str', width: 300 },
    {
        title: 'View more',
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
        if (localStorage.getItem('reactions') !== null){
            this.count = JSON.parse(localStorage.getItem('reactions')).length;
        }
        else {
            this.count = 0;
        }
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
                this.$message.error(error.message);
            });
    },
    components:{
        sidebar,
        kcat
    },
    data() {
        return {
            defaultActivate: ['2'],
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
            drawerVisible: false,
            drawerNumber:'',
            drawerData: [],
            count: null,
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
        async viewKcat(ec_number){
            axios.post('/api/search/kcat', {
                'ecNumber': ec_number})
                .then(response => {
                    this.drawerVisible = true;
                    this.drawerNumber = ec_number;
                    this.drawerData = response.data;})
                .catch(error => {
                    console.error(error);
                    this.$message.error(error.message);
                });
        },
        handleVisibleChange(newVisible) {
            this.drawerVisible = newVisible;
        },
        toBuild(){
            window.location.href = '/buildReactions';
        },
        handleAdd(data){
            this.count = data;
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
