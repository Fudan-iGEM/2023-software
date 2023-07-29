<template>
    <a-layout id="app" style="min-height: 100vh">
        <a-layout-sider v-model="collapsed" collapsible width="300">
            <div class="logo">
                <p style="font-size: 40px;text-align: center;overflow: hidden">aaaaaaa</p>
            </div>
            <a-menu theme="dark" mode="inline" :default-selected-keys="['1']">
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
                <a-table
                    :columns="columns"
                    :data-source="data"
                    :scroll="{ x: 1500, y: 600 }"
                    style="width: 95%"
                    bordered
                >
                    <p slot="title" style="font-weight: 700;font-size: 1rem">
                        Your Search result of {{searchQuery}} on {{searchType}}:
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
const columns = [
    { title: 'Full Name', width: 100, dataIndex: 'name', key: 'name', fixed: 'left' },
    { title: 'Age', width: 100, dataIndex: 'age', key: 'age', fixed: 'left' },
    { title: 'Column 1', dataIndex: 'long', key: '1', width: 150, ellipsis: true, },
    { title: 'Column 2', dataIndex: 'address', key: '2', width: 150 },
    { title: 'Column 3', dataIndex: 'address', key: '3', width: 150 },
    { title: 'Column 4', dataIndex: 'address', key: '4', width: 150 },
    { title: 'Column 5', dataIndex: 'address', key: '5', width: 150 },
    { title: 'Column 6', dataIndex: 'address', key: '6', width: 150 },
    { title: 'Column 7', dataIndex: 'address', key: '7', width: 150 },
    { title: 'Column 7', dataIndex: 'address', key: '8', width: 150 },
    { title: 'Column 7', dataIndex: 'address', key: '9', width: 150 },
    {
        title: 'Action',
        key: 'operation',
        fixed: 'right',
        width: 100,
        scopedSlots: { customRender: 'action' },
    },
];

const data = [];
for (let i = 0; i < 100; i++) {
    data.push({
        key: i,
        name: `Edrward ${i}`,
        age: 32,
        address: `London Park no. ${i}`,
        long:'London Park no. ${i}' * i,
    });
}
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
                console.log(response.data);})
            .catch(error => {
                console.error(error);
            });
    },
    data() {
        return {
            collapsed: false,
            searchResults: [],
            data,
            columns,
            searchType: localStorage.getItem('searchType'),
            searchQuery: localStorage.getItem('searchQuery'),
        };
    },
    methods: {
        toSearch() {
            window.location.href = '/search';
        },
        toGitlab() {
            window.open('https://gitlab.igem.org/2023/software-tools/fudan')
        },
        toWiki() {
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
