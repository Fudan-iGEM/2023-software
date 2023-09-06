<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',justifyContent:'flex-start',alignItems:'center',flexDirection:'column' }">
                    <a-steps :current="curStep" size="small" style="width: 80%;margin-top: 2rem">
                        <a-step title="Input CDS Sequence" />
                        <a-step title="Running RAP Builder" />
                        <a-step title="Download GeneBank format pRAP sequence" />
                    </a-steps>
                    <a-form :form="form" @submit="handleSubmit" layout='horizontal' style="width: 80%" v-if="curStep===0">
                        <a-form-item v-for="(reaction, index) in reactionData" :key="index" :label="reaction.ec_number" has-feedback>
                            <a-textarea
                                v-decorator="[
                                      reaction.id,
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please input coding sequence!',
                                          },
                                        ],
                                      },
                                    ]"
                                :placeholder="'Coding Sequence of EC' + reaction.ec_number"
                                :rows="3"
                            />
                        </a-form-item>
                        <a-form-item>
                            <a-button type="primary" html-type="submit">
                                Submit
                            </a-button>
                        </a-form-item>
                    </a-form>
                    <div v-if="curStep===1" style="position: absolute;top: 50%">
                        <a-spin size="large" tip="🔧It's running now, this may take take a few seconds to a few minutes."/>
                    </div>
                    <div v-if="curStep===2" style="position: absolute;top: 50%">
                        <h1>✅Your file is in the process of being downloaded, if not, please click <a :href="url">here</a> to download manually.</h1>
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
import sidebar from "@/components/sidebar.vue";
import axios from "axios";
export default {
    components:{
        sidebar
    },
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'sequences' });
    },
    created() {
        if (localStorage.getItem('reactions') === null){
            this.$message.warn('There is no reaction added, please add reactions!');
            setTimeout(function() {
                window.location.href = '/buildReactions';
            }, 4500);
        }
        if (localStorage.getItem('optimalRatio') !== null){
            this.optimalRatio = JSON.parse(localStorage.getItem('optimalRatio'));
            this.getReactionData(this.optimalRatio);
        }
        else {
            this.$message.warn('There is no reaction built, please build reactions!');
            setTimeout(function() {
                window.location.href = '/buildReactions';
            }, 4500);
        }
    },
    data() {
        return {
            defaultActivate:['5'],
            curStep:0,
            reactionData:null,
            url:null
        };
    },
    methods:{
        async getReactionData(optimalRatio){
            axios.post('/api/rap/reactionData', {
                'optimalRatio':optimalRatio})
                .then(response => {
                    this.reactionData = response.data})
                .catch(error => {
                    console.error(error);
                    this.$message.error(error.message);
                });
        },
        async handleSubmit(e){
            e.preventDefault();
            this.form.validateFieldsAndScroll((err, values) => {
                if (!err) {
                    const formData = [];
                    const regex = /^[ATCGatcgUu]+$/;
                    for (let key in values){
                        if (!regex.test(values[key])){
                            this.$message.warn('The input sequence must be a valid base sequence!');
                            return;
                        }
                        else {
                            let reaction={};
                            reaction['id'] = key;
                            reaction['sequence'] = values[key].toUpperCase();
                            for (let i = 0; i < this.optimalRatio.length; i++) {
                                if (key in this.optimalRatio[i]) {
                                    reaction['optimalRatio'] = this.optimalRatio[i][key];
                                    break;
                                }
                            }
                            for (let i = 0; i < this.reactionData.length; i++){
                                if (this.reactionData[i].id === key){
                                    reaction['ec_number'] = this.reactionData[i].ec_number;
                                    break;
                                }
                            }
                            formData.push(reaction);
                        }
                    }
                    this.curStep = 1;
                    axios.post('/api/rap/build', {
                        formData})
                        .then(response => {
                            if (response.data) {
                                this.$message.success(response.data.message);
                                this.taskID =  response.data.taskID;
                                let filename = this.taskID + '.gb';
                                this.url = '/download/' + filename
                                console.log(filename);
                                this.curStep = 2;
                                window.open(this.url);
                                this.form.resetFields();
                            }})
                        .catch(error => {
                            console.error(error);
                            this.$message.error(error.message);
                        });
                }
            });
        },
    }
};
</script>

<style scoped>
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
