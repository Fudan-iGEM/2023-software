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
                <a slot="action" slot-scope="text, record">
                    <a-icon type="plus-circle" @click="addKcat(record.database_id)" /></a>
            </a-table>
        </a-drawer>
</template>
<script>
const columns = [
    { title: 'KineticHub ID',
        width: 200,
        dataIndex: 'database_id',
        key: 'database_id',
        fixed: 'left',
        sorter: (a, b) => a.database_id - b.database_id },
    { title: 'Kcat (1/s)', width: 100, dataIndex: 'kcat', key: 'kcat', fixed: 'left', sorter: (a, b) => a.kcat - b.kcat },
    { title: 'Species',
        dataIndex: 'species',
        key: 'species',
        width: 200,
        scopedSlots: {
          customRender: 'species' },
        sorter: (a, b) => a.species.charCodeAt(2) - b.species.charCodeAt(2)
    },
    { title: 'Annotation', dataIndex: 'meta', key: 'meta', width: 150 },
    { title: 'References', dataIndex: 'refs', key: 'refs', width: 250, scopedSlots: { customRender: 'refs' } },
    { title: 'Substrate', dataIndex: 'substrate', key: 'substrate', width: 150,
        sorter: (a, b) => a.substrate.charCodeAt(2) - b.substrate.charCodeAt(2)},
    {
        title: 'Add',
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
        addKcat(database_id){
            if (localStorage.getItem('reactions') !== null) {
                let reactions = JSON.parse(localStorage.getItem('reactions'))
                if (reactions.some(item => item.ec_number === this.ec_number)){
                    this.$message.info('You have added this reaction!')
                }
                else {
                    const obj = {}
                    obj['ec_number'] = this.ec_number;
                    obj['id'] = database_id
                    reactions.push(obj);
                    localStorage.setItem('reactions', JSON.stringify(reactions));
                    this.$emit('update-reactions', reactions.length);
                    this.$message.success('Successfully add record ' + database_id.toString())
                }
            } else {
                const obj = {}
                obj['ec_number'] = this.ec_number;
                obj['id'] = database_id
                localStorage.setItem('reactions', JSON.stringify([obj]));
                this.$emit('update-reactions', 1);
                this.$message.success('Successfully add record ' + database_id.toString())
            }
        }
    },
};
</script>