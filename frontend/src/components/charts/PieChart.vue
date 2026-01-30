<script setup>
import { computed } from "vue";
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});

const chartData = computed(() => ({
  labels: props.data.map((item) => item.category__name),
  datasets: [
    {
      data: props.data.map((item) => item.total),
      backgroundColor: props.data.map((item) => item.category__color),
      borderWidth: 2,
      borderColor: "#ffffff",
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "bottom",
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const value = context.parsed;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(1);
          return `${context.label}: ${value.toLocaleString()} VND (${percentage}%)`;
        },
      },
    },
  },
};
</script>

<template>
  <div class="w-full h-64">
    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>
