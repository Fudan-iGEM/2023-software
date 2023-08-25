<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout v-if="isReactions">
            <a-layout-content style="margin: 0">
                <div :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',justifyContent:'center',alignItems:'flex-start' }">
                    <div style="width: 80%;height: 100%">
                        <p style="font-size: 3rem;font-weight: 700;margin-bottom: 1rem">Build your reactions</p>
                        <div class="build-form">
                            <p>Please input ratio of product to substrate stoichiometry for your reactions according to EC number</p>
                            <a-form
                                :form="form"
                                @submit="handleSubmit"
                                layout="inline"
                            >
                                <a-form-item v-for="(reaction, index) in reactions" :key="index" :label="reaction.ec_number">
                                    <a-input-number
                                        v-decorator="[
                                          reaction.id,
                                          { rules: [{ required: true, message: 'Please input stoichiometric values!' }] },
                                        ]"
                                        :min="0.01"
                                    />
                                </a-form-item>
                                <a-form-item>
                                    <a-button type="primary" html-type="submit">
                                        Submit
                                    </a-button>
                                </a-form-item>
                            </a-form>
                        </div>
                        <div style="width: 60%">
                            <a-tabs>
                                <a-tab-pane v-for="(reaction, index) in reactionData" :key="index" :tab="reaction.ec_number">
                                    <p>KineticHub ID: {{reaction.id}}</p>
                                    <p>Name: {{reaction.name}}</p>
                                    <p>Species: {{JSON.parse(reaction.species).join()}}</p>
                                    <p>Substrate: {{reaction.substrate}}</p>
                                    <p>Formula: {{reaction.str}}</p>
                                </a-tab-pane>
                                <a-button slot="tabBarExtraContent" @click="clearReactions()">
                                    Clear all
                                </a-button>
                            </a-tabs>
                        </div>
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
import axios from "axios";
export default {
    components:{
        sidebar
    },
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'build' });
    },
    created() {
        if (localStorage.getItem('reactions') !== null){
            this.isReactions = true;
            this.reactions = JSON.parse(localStorage.getItem('reactions'));
            this.getReactionData(this.reactions);
        }
        else {
            this.$message.warn('There is no reaction added, please add reactions');
            this.isReactions = false;
            setTimeout(function() {
                window.location.href = '/search';
            }, 4500);
        }
    },
    data() {
        return {
            defaultActivate:['3'],
            isReactions: null,
            reactions: null,
            reactionData:null
        };
    },
    methods:{
        async getReactionData(reactions){
            axios.post('/api/build/reactionData', {
                'reactions':reactions})
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
                    console.log('Received values of form: ', values);
                    axios.post('/api/buildReactions', {
                        values})
                        .then(response => {
                            if (response.data) {
                                localStorage.setItem('optimalRatio', response.data);
                                setTimeout(function() {
                                    window.location.href = '/RAPBuilder';
                                }, 5000);
                                this.$message.success('Successfully build all reactions, you can run step 2!');
                            }})
                        .catch(error => {
                            console.error(error);
                            this.$message.error(error.message);
                        });
                }
            });
        },
        clearReactions(){
            localStorage.removeItem('reactions');
            setTimeout(function() {
                window.location.href = '/search';
            }, 5000);
            this.$message.success('All reactions are cleared, will redirect to search page in 5s')
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
.build-form p {
    margin: 0;
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
