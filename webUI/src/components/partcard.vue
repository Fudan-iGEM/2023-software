<template>
    <a-list item-layout="vertical" size="large" :pagination="pagination" :data-source="listData">
        <a-list-item slot="renderItem" :key="index" slot-scope="item,index">
            <a-list-item-meta
                :description="item.description">
                <a slot="title" style="color: #e37654">{{item.number}}: {{item.name}}</a>
            </a-list-item-meta>
            <p>{{ item.content }}</p>
            <p style="color: gray">{{item.cites}} cited · {{item.twinsNum}} twin(s) · {{item.seqLength}} bp · {{item.isFavorite ==='True' ? 'Favorite Part · ':''}}
            {{item.released ==='Not Released' ? item.released+' · ':''}}{{item.date}}
            </p>
        </a-list-item>
    </a-list>
</template>
<script>
export default {
    props:['listData'],
    data(){
        return{
            pagination: {
                onChange: page => {
                    console.log(page);
                },
                pageSize: 10,
            },
        }
    }
}
</script>
<style scoped>
</style>