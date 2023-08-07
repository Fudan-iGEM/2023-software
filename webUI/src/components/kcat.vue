<template>
        <a-drawer
                :title= "ec_number"
                placement="right"
                width="80%"
                :visible="visible"
                @close="onClose"
        >
            <a-table
                    :columns="columns"
                    :data-source="data"
                    :scroll="{ x: 1200, y: 600 }"
                    style="width: 95%"
            >
                <span slot="species" slot-scope="species">
                  <p
                          v-for="tag in JSON.parse(species)"
                          :key="tag"
                  >
                    {{ tag }}
                  </p>
                </span>
                <span slot="refs" slot-scope="refs">
                  <p
                          v-for="ref in JSON.parse(refs)"
                          :key="ref"
                  >
                    {{ ref }}
                  </p>
                </span>
                <a slot="action"><a-icon type="plus-circle" /></a>
            </a-table>
        </a-drawer>
</template>
<script>
const columns = [
    { title: 'KineticHub ID', width: 200, dataIndex: 'database_id', key: 'database_id', fixed: 'left' },
    { title: 'Kcat', width: 100, dataIndex: 'kcat', key: 'kcat', fixed: 'left', sorter: (a, b) => a.kcat - b.kcat },
    { title: 'Species', dataIndex: 'species', key: 'species', width: 200, scopedSlots: { customRender: 'species' }},
    { title: 'Annotation', dataIndex: 'meta', key: 'meta', width: 150 },
    { title: 'References', dataIndex: 'refs', key: 'refs', width: 200, scopedSlots: { customRender: 'refs' } },
    { title: 'Substrate', dataIndex: 'substrate', key: 'substrate', width: 200,},
    {
        title: 'Action',
        key: 'operation',
        fixed: 'right',
        scopedSlots: { customRender: 'action' },
    },
];
export default {
    data() {
        return {
            columns,
        };
    },
    props:['ec_number','visible','data'],
    methods: {
        onClose() {
            this.$emit('onClose', false);
        },
    },
};
</script>