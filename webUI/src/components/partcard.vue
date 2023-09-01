<template>
    <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
        <a-list-item slot="renderItem" :key="index" slot-scope="item,index">
            <a-list-item-meta>
                <p slot="description" style="color:gray;">Year: {{item.year}} > Team: {{item.team}} > Designer: {{item.designer}} > Type: {{item.type}}</p>
                <a slot="title" style="color: #e37654">{{item.number}}: {{item.name}}</a>
            </a-list-item-meta>
            <p v-html="highlight(item.content)"></p>
            <p style="color: gray">{{item.cites}} cited · {{item.twinsNum}} twin(s) · {{item.seqLength}} bp · {{item.isFavorite ==='True' ? 'Favorite Part · ':''}}
            {{item.released ==='Not Released' ? item.released+' · ':''}}{{item.date}}
            </p>
        </a-list-item>
    </a-list>
</template>
<script>
export default {
    props:['listData','searchQuery'],
    data(){
        return{
            pagination: {
                onChange: page => {
                    console.log(page);
                },
                pageSize: 10,
            },
        }
    },
    methods:{
        highlight(content){
            const regex = new RegExp(this.searchQuery, "gi");
            return content.replace(regex, '<span style="color:red;">$&</span>') + '...';
        }
    }
}
</script>
<style scoped>
</style>