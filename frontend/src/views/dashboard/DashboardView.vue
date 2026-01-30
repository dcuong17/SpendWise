<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Navbar from '@/components/layout/Navbar.vue'
import PieChart from '@/components/charts/PieChart.vue'
import LineChart from '@/components/charts/LineChart.vue'
import {
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  WalletIcon,
  CreditCardIcon,
} from '@heroicons/vue/24/outline'
import { format } from 'date-fns'
import api from '@/services/api'

const authStore = useAuthStore()

const stats = ref({
  income: 0,
  expenses: 0,
  balance: 0,
  transaction_count: 0,
})

const categoryData = ref(null)
const trendData = ref(null)
const recentTransactions = ref([])

const user = computed(() => authStore.user)

// Fetch dashboard data
onMounted(async () => {
  await Promise.all([
    fetchStats(),
    fetchCategoryData(),
    fetchTrendData(),
    fetchRecentTransactions(),
  ])
})

const fetchStats = async () => {
  try {
    const response = await api.get('/analytics/dashboard/')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

const fetchCategoryData = async () => {
  try {
    const response = await api.get('/analytics/expenses-by-category/')
    categoryData.value = response.data
  } catch (error) {
    console.error('Failed to fetch category data:', error)
  }
}

const fetchTrendData = async () => {
  try {
    const response = await api.get('/analytics/spending-trend/')
    trendData.value = response.data
  } catch (error) {
    console.error('Failed to fetch trend data:', error)
  }
}

const fetchRecentTransactions = async () => {
  try {
    const response = await api.get('/transactions/?ordering=-date&page_size=5')
    recentTransactions.value = response.data.results
  } catch (error) {
    console.error('Failed to fetch recent transactions:', error)
  }
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
  }).format(amount)
}

const formatDate = (date) => {
  return format(new Date(date), 'MMM dd, yyyy')
}
</script>


<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-1 text-sm text-gray-500">Welcome back, {{ user?.first_name }}!</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Income Card -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Income</p>
              <p class="text-2xl font-bold text-success-600">
                {{ formatCurrency(stats.income) }}
              </p>
            </div>
            <div class="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center">
              <ArrowTrendingUpIcon class="h-6 w-6 text-success-600" />
            </div>
          </div>
        </div>

        <!-- Expense Card -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Expenses</p>
              <p class="text-2xl font-bold text-danger-600">
                {{ formatCurrency(stats.expenses) }}
              </p>
            </div>
            <div class="w-12 h-12 bg-danger-100 rounded-full flex items-center justify-center">
              <ArrowTrendingDownIcon class="h-6 w-6 text-danger-600" />
            </div>
          </div>
        </div>

        <!-- Balance Card -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Balance</p>
              <p class="text-2xl font-bold text-primary-600">
                {{ formatCurrency(stats.balance) }}
              </p>
            </div>
            <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <WalletIcon class="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <!-- Transactions Count -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Transactions</p>
              <p class="text-2xl font-bold text-gray-900">{{ stats.transaction_count }}</p>
            </div>
            <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
              <CreditCardIcon class="h-6 w-6 text-gray-600" />
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Expenses by Category (Pie Chart) -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Expenses by Category</h3>
          <PieChart :data="categoryData" />
        </div>

        <!-- Spending Trend (Line Chart) -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Spending Trend (Last 30 Days)</h3>
          <LineChart :data="trendData" />
        </div>
      </div>

      <!-- Recent Transactions -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">Recent Transactions</h3>
          <router-link to="/transactions" class="text-sm text-primary-600 hover:text-primary-700">
            View all →
          </router-link>
        </div>
        
        <div class="space-y-4">
          <!-- Transaction Item (Template) -->
          <div
            v-for="transaction in recentTransactions"
            :key="transaction.id"
            class="flex items-center justify-between py-3 border-b last:border-b-0"
          >
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-full flex items-center justify-center"
                   :style="{ backgroundColor: transaction.category_color + '20' }">
                <span class="text-xl">{{ transaction.category_icon }}</span>
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ transaction.description }}</p>
                <p class="text-sm text-gray-500">{{ transaction.category_name }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="font-semibold"
                 :class="transaction.type === 'income' ? 'text-success-600' : 'text-danger-600'">
                {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
              </p>
              <p class="text-sm text-gray-500">{{ formatDate(transaction.date) }}</p>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="recentTransactions.length === 0" class="text-center py-8">
            <p class="text-gray-500">No transactions yet</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

