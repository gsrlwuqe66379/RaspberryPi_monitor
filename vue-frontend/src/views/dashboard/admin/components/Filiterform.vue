<template>
    <div class="filter-form">
        <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px"
            style="width: 400px; margin-left:50px;">
            <el-form-item label="开始时间">
                <el-col :span="11">
                    <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"
                        :picker-options="{
                            disabledDate(time) {
                                const now = new Date();
                                return time.getTime() > now.getTime();
                            }
                        }" />
                </el-col>
                <el-col class="line" :span="2">-</el-col>
                <el-col :span="11">
                    <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
                </el-col>
            </el-form-item>
            <el-form-item label="结束时间">
                <el-col :span="11">
                    <el-date-picker type="date" placeholder="选择日期" v-model="temp.date3" style="width: 100%;"
                        :picker-options="{
                            disabledDate(time) {
                                const now = new Date();
                                return (form.date1 && time.getTime() < form.date1.getTime()) || time.getTime() > now.getTime();
                            }
                        }" />
                </el-col>
                <el-col class="line" :span="2">-</el-col>
                <el-col :span="11">
                    <el-time-picker placeholder="选择时间" v-model="temp.date4" style="width: 100%;" :picker-options="{
                        disabledTime(time) {
                            const now = new Date();
                            return (form.date2 && time.getTime() < form.date2.getTime()) || time.getTime() > now.getTime();
                        }
                    }" />
                </el-col>
            </el-form-item>
            <el-select></el-select>
        </el-form>
        <el-button type="primary">commit</el-button>
    </div>
</template>

<script>


export default {
    data() {
        return {
            form: {
                date1: '',
                date2: '',
                date3: '',
                date4: ''
            },
            temp: {
                date1: '',
                date2: '',
                date3: '',
                date4: ''
            },
            rules: {
                date1: [
                    { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
                ],
                date2: [
                    { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
                ],
                date3: [
                    { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
                ],
                date4: [
                    { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
                ]
            }
        }
    },
    methods: {
        handleQueryData() {
            this.dialogFormVisible = true
        }
    },
}

</script>

<style lang="scss" scoped></style>
