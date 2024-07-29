<template>
    <div>
        <div ref="chart" style="width: 100%; height: 400px;"></div>
    </div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue';
import * as echarts from 'echarts';
import {
    parseISO,
    format,
    startOfMonth,
    endOfMonth,
    eachDayOfInterval,
    eachWeekOfInterval,
    getWeek,
    subDays
} from 'date-fns';

const props = defineProps({
    historys: Array
});

const chart = ref(null);
let myChart = null;

const processData = () => {
    const now = new Date();
    const weekStart = subDays(now, 7);
    const weekEnd = new Date();
    const monthStart = startOfMonth(now);
    const monthEnd = endOfMonth(now);

    const daysOfWeek = eachDayOfInterval({start: weekStart, end: weekEnd});
    const weeksOfMonth = eachWeekOfInterval({start: monthStart, end: monthEnd}, {weekStartsOn: 1});

    const dailyData = {};
    const weeklyData = {};

    daysOfWeek.forEach(day => {
        dailyData[format(day, 'yyyy-MM-dd')] = 0;
    });

    weeksOfMonth.forEach(week => {
        weeklyData[getWeek(week, {weekStartsOn: 1})] = 0;
    });

    props.historys.forEach(history => {
        const createTime = parseISO(history.create_time);
        const dayKey = format(createTime, 'yyyy-MM-dd');
        const weekKey = getWeek(createTime, {weekStartsOn: 1});

        if (dayKey in dailyData) {
            dailyData[dayKey]++;
        }

        if (weekKey in weeklyData) {
            weeklyData[weekKey]++;
        }
    });

    return {
        dailyData: Object.values(dailyData),
        weeklyData: Object.values(weeklyData),
        daysOfWeek: daysOfWeek.map(day => format(day, 'MM-dd')),
        weeksOfMonth: weeksOfMonth.map(week => `Week ${getWeek(week, {weekStartsOn: 1})}`)
    };
};

const renderChart = () => {
    const {dailyData, weeklyData, daysOfWeek, weeksOfMonth} = processData();

    const option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['Daily', 'Weekly']
        },
        xAxis: [
            {
                type: 'category',
                data: daysOfWeek,
                axisLabel: {
                    rotate: 45
                }
            },
            {
                type: 'category',
                data: weeksOfMonth,
                axisLabel: {
                    rotate: 45
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: 'Daily',
                type: 'line',
                data: dailyData
            },
            {
                name: 'Weekly',
                type: 'line',
                data: weeklyData
            }
        ]
    };

    myChart.setOption(option);
};

onMounted(() => {
    console.log(props.historys)
    myChart = echarts.init(chart.value);
    renderChart();
});

watch(() => props.historys, () => {
    renderChart();
});
</script>

<style scoped>
</style>
