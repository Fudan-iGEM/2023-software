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
                        <a-form-item label="Mode" has-feedback>
                            <a-select
                                    v-decorator="[
                                      'mode',
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please select design mode!',
                                          },
                                        ],
                                        initialValue: 'rbs'
                                      },
                                    ]"
                            >
                                <a-select-option value="rbs">
                                    RBS design mode
                                </a-select-option>
                                <a-select-option value="stem_loop">
                                    Stem loop design mode
                                </a-select-option>
                            </a-select>
                        </a-form-item>
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
                                        initialValue: reaction.sequence
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
    data() {
        return {
            defaultActivate:['5'],
            curStep:0,
            reactionData:[{id: "76812", sequence:"atggcggctattaatacaaaagttaagaaagcggttatcccggtggcaggccttggcacaagaatgcttccggcaacaaaagcaattccgaaagaaatgcttccgctggttgataaaccgcttattcaatatgtggtgaatgaatgcattgcggcaggaattacagaaattgttctggtgacacatagctcaaaaaatagcattgaaaaccatttcgacacaagctttgaactggaagcgatgctggaaaaaagagtgaaaagacagctgctggatgaagtgcagagcatttgtccgccgcatgttacaattatgcaagtgagacaaggcctggcaaaaggacttggccatgcggttctgtgcgcgcatccggttgttggagatgagccggttgcagttattctgccggatgtgattctggatgaatatgaatcagacctgtcacaggataatctggcggaaatgattagaagatttgatgaaacaggccatagccaaattatggtggagccggttgcggatgtgacagcatatggagttgttgattgcaaaggagtggaactggcaccgggagaaagcgttccgatggtgggcgtggttgaaaaaccgaaagcagatgtggcaccgagcaatctggcgattgttggcagatatgttctgtcagcggatatttggccgctgctggcaaaaacaccgccgggcgcaggcgatgaaattcaacttacagatgcaattgatatgctgattgaaaaagaaacagtggaagcgtatcatatgaaaggaaaaagccatgattgcggaaataagcttggatatatgcaggcgtttgttgaatatggaattagacataatacgctgggcacagagttcaaagcatggcttgaagaagaaatgggcattaagaaataa", optimalRatio: 1, ec_number: "2.7.7.9"},
                {id: "76813", sequence: "atggcaattcataacagagcaggccaaccggcacaacagtcagaccttattaatgtggcacagcttacagcacaatattatgttcttaaaccggaagcaggaaatgcagaacatgcagttaaatttggaacaagcggacatagaggatcagcggcgagacatagctttaatgaaccgcatattctggcgattgcacaggcgattgcggaagaaagagcgaaaaatggaattacaggcccgtgctatgttggaaaagatacacatgcgctgagcgaaccggcattcatttcagtgcttgaagtgctggcagcgaatggcgtggatgtgattgtgcaggaaaataatggctttacaccgacaccggcagttagcaatgcgattctggttcataataagaaaggcggaccgctggcggatggcattgttattacaccgagccataatccgccggaagatggaggcattaagtataatccgccgaatggaggaccggcggatacaaatgttacaaaagtggttgaagatagagcgaatgcgcttcttgcggatggactgaaaggcgttaaaagaattagcctggatgaagcaatggcaagcggccatgttaaagaacaagaccttgtgcagccgtttgtggaaggccttgcagatattgttgatatggcggcaattcagaaagcaggccttacacttggagttgatccgcttggaggctcaggaattgaatattggaaaagaattggcgaatactataaccttaacctgacaattgtgaatgatcaagttgatcaaacattcagattcatgcatctggataaagatggcgcgattagaatggattgttcaagcgaatgcgcaatggcgggactgctggcgcttagagataaatttgatctggcgtttgcgaatgatccggattatgatagacatggcattgttacaccggcgggacttatgaatccgaatcattatcttgcagttgcgattaattacctttttcaacatagaccgcaatggggcaaagatgtggcggtgggaaaaacactggtgagcagcgcaatgattgatagagtggttaatgatctgggcagaaaactggttgaagttccggtgggctttaaatggtttgttgatggactgtttgatggctcatttggctttggaggagaagaatcagcgggagcgtcatttctgagatttgatggcacaccgtggagcacagataaagatggaattattatgtgcctgcttgcagcagaaattacagcagttacaggcaaaaatccgcaagaacattataatgaactggcgaaaagatttggagcgccgagctataatagacttcaagcggcggcaacatcagcacaaaaagcggcactttcaaaactgagcccggaaatggttagcgcaagcacacttgcgggagatccgattacagcgagacttacagcagcgccgggcaatggcgcatcaattggcggactgaaagttatgacagataatggctggtttgcggcaagaccgtcaggcacagaagatgcatataaaatctattgcgaatcattcctgggagaagaacatagaaaacagattgaaaaagaggcggttgaaattgtttcagaagttcttaaaaacgcataa", optimalRatio: 0.26201153106982705, ec_number: "5.4.2.2"}],
            optimalRatio:[{"76812":1},{"76813":0.26201153106982705}],
            url:null,
            design:'rbs'
        };
    },
    methods:{
        async handleSubmit(e){
            e.preventDefault();
            this.form.validateFieldsAndScroll((err, values) => {
                if (!err) {
                    let mode = values.mode;
                    delete values.mode;
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
                    if (mode==='rbs'){
                        axios.post('/api/rap/build', {
                            formData})
                            .then(response => {
                                if (response.data) {
                                    this.$message.success(response.data.message);
                                    this.taskID =  response.data.taskID;
                                    let filename = this.taskID + '.zip';
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
                    if(mode==='stem_loop'){
                        axios.post('/api/rap/build/stemLoop', {
                            formData})
                            .then(response => {
                                if (response.data) {
                                    this.$message.success(response.data.message);
                                    this.taskID =  response.data.taskID;
                                    let filename = this.taskID + '.zip';
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
