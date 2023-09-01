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
                                Search parts by:
                                <a-radio-group
                                        :defaultValue="searchType"
                                        v-decorator="[
                                      'type',
                                      { rules: [{ required: true, message: 'Please select a search type!' }] },
                                    ]"
                                >
                                    <a-radio-button value="id">
                                        ID
                                    </a-radio-button>
                                    <a-radio-button value="sequence">
                                        Sequence
                                    </a-radio-button>
                                    <a-radio-button value="designer">
                                        Designer
                                    </a-radio-button>
                                    <a-radio-button value="team">
                                        Team
                                    </a-radio-button>
                                    <a-radio-button value="content">
                                        Content
                                    </a-radio-button>
                                </a-radio-group>
                            </a-form-item>
                        </a-form>
                    </div>
                    <partcard :list-data="listData">
                    </partcard>
                </div>
            </a-layout-content>
            <a-layout-footer style="text-align: center;padding-top: 12px;padding-bottom: 12px">
                RAP ©2023 Created by mistyfield
            </a-layout-footer>
        </a-layout>
    </a-layout>
</template>
<script>
import sidebar from "@/components/sidebar.vue";
import partcard from "@/components/partcard.vue";
const listData = [];
for (let i = 0; i < 23; i++) {
    listData.push({
        number: 'BBa_114514',
        name: '1323232vfvevwevrv',
        avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
        date:'2013-4-5',
        seqLength:100,
        cites:2,
        twinsNum:0,
        isFavorite: 'True',
        released: 'Not Released',
        description:
            'Ant Design, a design language for background applications, is refined by Ant UED Team.',
        content:
            'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
    });
}
export default {
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'search' });
    },
    created() {
        const searchType = localStorage.getItem('partHubType');
        const searchQuery = localStorage.getItem('partHubType');
        if (!searchType || !searchQuery) {
            window.location.href = '/parthub2';
        }
        /*axios.post('/api/search/reaction', {
            'searchType': searchType,
            'searchQuery':searchQuery})
            .then(response => {
                this.data = response.data})
            .catch(error => {
                console.error(error);
                this.$message.error(error.message);
            });*/
    },
    components:{
        partcard,
        sidebar,
    },
    data() {
        return {
            defaultActivate: ['10'],
            searchResults: [],
            searchType: localStorage.getItem('partHubType'),
            searchQuery: localStorage.getItem('partHubQuery'),
            typeDict:{
                'id': 'ID',
                'name': 'Name',
                'sequence': 'Sequence',
                'substrates': 'Substrate',
                'products': 'Products'
            },
            listData,
        };
    },
    methods: {
        async handleSubmit(e) {
            e.preventDefault();
            this.form.validateFields(async (err, values) => {
                if (!err) {
                    console.log(values)
                    if (values.type==='sequence'){
                        const regex = /^[ATCGatcgUu]+$/;
                        if (!regex.test(values.query)){
                            this.$message.warn('The input sequence must be a valid base sequence!');
                            return;
                        }
                    }
                    localStorage.setItem('partHubQuery', values.query);
                    localStorage.setItem('partHubType', values.type);
                    window.location.href = '/parts'
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
