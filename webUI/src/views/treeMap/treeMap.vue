<template>
    <a-layout id="app" style="min-height: 100vh">
        <sidebar :default-activate="defaultActivate"></sidebar>
        <a-layout>
            <a-layout-content style="margin: 0">
                <div
                :style="{ padding: '0', background: '#fff6f0', minHeight: '100%',display:'flex',flexDirection:'row',justifyContent:'flex-start',alignItems:'center' }"
                >
                    <div style="margin-left: 1rem;width: 60%">
                        <h1 style="color: #e37654">Your Part map of {{curPart}}:</h1>
                        <p>Scroll to zoom the canvas and drag to move the nodes. Click the circle to display the part details and double click to go to the part page.</p>
                        <div id="viz" style="display: flex;justify-content: center; align-items: center; "><a-spin :spinning="loading" tip="loading" size="large"></a-spin></div>
                    </div>
                    <div style="margin-left: 1rem;width: 35%">
                        <a-card :title="title">
                            <template slot="actions">
                                <a><a-icon type="download" /> Download sequence</a>
                                <a href=""><a-icon type="link" /> View in iGEM Parts Registry</a>
                            </template>
                        </a-card>
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
import NeoVis from 'neovis.js';
import sidebar from "@/components/sidebar.vue";
export default {
    components:{
        sidebar
    },
    created() {
        const curPart = localStorage.getItem('curPart');
        if (!curPart){
            window.location.href = '/parts';
        }
        else {
            this.curPart = curPart;
        }
    },
    data() {
        return {
            defaultActivate:['10'],
            curPart:null,
            title:' ',
            loading:true,
        };
    },
    mounted() {
        this.draw();
    },
    methods: {
        draw() {
            var viz;
            var config = {
                containerId: "viz",
                neo4j: {
                    serverUrl: "bolt://54.169.242.254:7687",
                    serverUser: "neo4j",
                    serverPassword: "igem2023"
                },
                visConfig: {
                    nodes: {
                        shape: 'dot',
                        font: {
                            face:'HarmonyOS_Sans',
                        },
                    },
                    edges: {
                        arrows: {
                            to: {enabled: true}
                        },
                        color: '#CCC',
                        font: {
                            face:'HarmonyOS_Sans',
                        },
                    },
                },
                labels: {
                    Part: {
                        label: "number",
                        color: 'color',
                        size:'nodesize'
                    }
                },
                relationships: {
                    'refers to': {
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                            static: {
                                label: 'refers to',
                            },
                        },
                    },
                    'twins': {
                        [NeoVis.NEOVIS_ADVANCED_CONFIG]: {
                            static: {
                                label: 'twins',
                            },
                        },
                    },
                },
                initialCypher: "MATCH p=()-->() RETURN p LIMIT 25"
            };
            viz = new NeoVis(config);
            var doubleClickLocked = false;
            viz.registerOnEvent("clickNode", () => {
                viz.network.on('doubleClick', function (properties) {
                    if (!doubleClickLocked) {
                        doubleClickLocked = true;
                        var ids = properties.nodes;
                        var clickedNodes = viz.nodes.get(ids);
                        if (clickedNodes) {
                            window.open(clickedNodes[0].raw.properties.url);
                        }
                        setTimeout(function () {
                            doubleClickLocked = false;
                        }, 300);
                    }
                });
            });
            viz.registerOnEvent("completed", ()=>{
                viz.network.on('stabilizationIterationsDone', function() {
                    this.loading=false;
                });
            });
            viz.render();
        },
    }
}
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
#viz{
    width: 100%;
    height: 700px;
    border: 0.2rem solid #963b29;
    border-radius: 5px;
}
</style>