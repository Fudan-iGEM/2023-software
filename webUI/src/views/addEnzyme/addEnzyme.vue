<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',justifyContent:'center',alignItems:'center' }">
                    <div style="text-align: center;height: 100%;width: 50%">
                        <p style="font-size: 3rem;font-weight: 700;">Add new enzyme record</p>
                        <a-form :form="form" @submit="handleSubmit" layout='vertical'>
                            <a-form-item label="EC number" has-feedback>
                                <a-select
                                    show-search
                                    :not-found-content="ec_fetching ? undefined : null"
                                    :default-active-first-option="false"
                                    option-filter-prop="children"
                                    :filter-option="filterOption"
                                    @search="fetchEC"
                                    v-decorator="[
                                      'ec_number',
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please input the EC number of the enzyme!',
                                          },
                                        ],
                                      },
                                    ]"
                                >
                                    <a-spin v-if="fetching" slot="notFoundContent" size="small" />
                                    <a-select-option v-for="d in ec_data" :key="d">
                                        {{ d }}
                                    </a-select-option>
                                </a-select>
                            </a-form-item>
                            <a-form-item label="Kcat (1/s)" has-feedback>
                                <a-input
                                    v-decorator="[
                                      'k_cat',
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please input the Kcat of the enzyme!',
                                          },
                                          {
                                            validator: isFloat,
                                          },
                                        ],
                                      },
                                    ]"
                                />
                            </a-form-item>
                            <a-form-item label="Species" has-feedback>
                                <a-select
                                    mode="tags"
                                    :not-found-content="false"
                                    v-decorator="[
                                      'species',
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please input the species of the enzyme!',
                                          },
                                        ],
                                      },
                                    ]"
                                >
                                </a-select>
                            </a-form-item>
                            <a-form-item label="Annotation">
                                <a-textarea v-decorator= "['meta']" placeholder="Like temperature, pH, etc." :rows="4" />
                            </a-form-item>
                            <a-form-item label="Your references, your group or your email" has-feedback>
                                <a-input
                                    v-decorator="[
                                      'refs',
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please input your group name or your email!',
                                          },
                                        ],
                                      },
                                    ]"
                                />
                            </a-form-item>
                            <a-form-item label="Substrate" has-feedback>
                                <a-input
                                    v-decorator="[
                                      'substrate',
                                      {
                                        rules: [
                                          {
                                            required: true,
                                            message: 'Please input the substrate of the enzyme!',
                                          },
                                        ],
                                      },
                                    ]"
                                />
                            </a-form-item>
                            <a-form-item>
                                <a-button type="primary" html-type="submit">
                                    Register to KineticHub
                                </a-button>
                            </a-form-item>
                        </a-form>
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
import debounce from 'lodash/debounce';
import axios from 'axios';
import sidebar from "@/components/sidebar.vue";
export default {
    components:{
        sidebar
    },
    data() {
        this.fetchEC = debounce(this.fetchEC, 800);
        return {
            defaultActivate: ['4'],
            ec_data: [],
            ec_fetching: false
        };
    },
    beforeCreate() {
        this.form = this.$form.createForm(this, { name: 'register' });
    },
    methods:{
        filterOption(input, option) {
            return (
                option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
            );
        },
        isFloat(rule, value, callback){
            if (value && isNaN(value)) {
                callback('The Kcat should be a numeric value!');
            } else {
                callback();
            }
        },
        handleSubmit(e) {
            e.preventDefault();
            this.form.validateFieldsAndScroll((err, values) => {
                if (!err) {
                    axios.post('/api/addEnzyme', {
                        values})
                        .then(response => {
                            if (response.data) {
                                this.$message.success(response.data.message);
                                this.form.resetFields();
                            }})
                        .catch(error => {
                            console.error(error);
                            this.$message.error(error.message);
                        });
                }
            });
        },
        fetchEC(value) {
            this.ec_fetching = true;
            if(value){
                axios.post('/api/addEnzyme/sug/ec_number', {
                    'ecNumber': value})
                    .then(response => {
                        if (response.data) {
                            this.ec_data = response.data;
                        }})
                    .catch(error => {
                        console.error(error);
                        this.$message.error(error.message);
                    });
            }
            this.ec_fetching = false;
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
