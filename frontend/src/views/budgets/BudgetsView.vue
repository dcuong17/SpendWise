<script setup>
import { ref, onMounted, computed } from 'vue'
import { format, addMonths, subMonths, startOfMonth } from 'date-fns'
import api from '@/services/api'
import Navbar from '@/components/layout/Navbar.vue'

const budgets = ref([])
const currentMonth = ref(startOfMonth(new Date()))
const showModal = ref(false)
const editingBudget = ref(null)

const currentMonthLabel = computed(() => {
  return format(currentMonth.value, 'MMMM yyyy')
})

onMounted(() => {
  fetchBudgets()
})

const fetchBudgets = async () => {
  try {
    const monthParam = format(currentMonth.value, 'yyyy-MM-dd')
    const response = await api.get(`/budgets/?month=${monthParam}`)
    budgets.value = response.data
  } catch (error) {
    console.error('Failed to fetch budgets:', error)
  }
}

const previousMonth = () => {
  currentMonth.value = subMonths(currentMonth.value, 1)
  fetchBudgets()
}

const nextMonth = () => {
  currentMonth.value = addMonths(currentMonth.value, 1)
  fetchBudgets()
}

const openAddModal = () => {
  editingBudget.value = null
  showModal.value = true
}

const editBudget = (budget) => {
  editingBudget.value = budget
  showModal.value = true
}

const deleteBudget = async (id) => {
  if (!confirm('Are you sure you want to delete this budget?')) return

  try {
    await api.delete(`/budgets/${id}/`)
    fetchBudgets()
  } catch (error) {
    console.error('Failed to delete budget:', error)
  }
}

const getProgressColor = (percentage) => {
  if (percentage >= 100) return 'bg-red-500'
  if (percentage >= 80) return 'bg-yellow-500'
  return 'bg-green-500'
}

const getTextColor = (percentage) => {
  if (percentage >= 100) return 'text-red-600 font-semibold'
  if (percentage >= 80) return 'text-yellow-600 font-semibold'
  return 'text-green-600 font-semibold'
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
  }).format(amount)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Budgets</h1>
          <p class="mt-1 text-sm text-gray-500">Plan and track your monthly budgets</p>
        </div>
        <button @click="openAddModal" class="btn-primary">
          + Add Budget
        </button>
      </div>

      <!-- Month Selector -->
      <div class="card mb-6">
        <div class="flex items-center justify-between">
          <button @click="previousMonth" class="btn-secondary">
            ← Previous
          </button>
          <h2 class="text-xl font-semibold text-gray-900">
            {{ currentMonthLabel }}
          </h2>
          <button @click="nextMonth" class="btn-secondary">
            Next →
          </button>
        </div>
      </div>

      <!-- Budgets Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Budget Card -->
        <div v-for="budget in budgets" :key="budget.id" class="card">
          <!-- Category Header -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-2">
              <span class="text-2xl">{{ budget.category_icon }}</span>
              <h3 class="font-semibold text-gray-900">{{ budget.category_name }}</h3>
            </div>
            <div class="flex space-x-2">
              <button @click="editBudget(budget)" class="text-primary-600 hover:text-primary-900">
                Edit
              </button>
              <button @click="deleteBudget(budget.id)" class="text-red-600 hover:text-red-900">
                Delete
              </button>
            </div>
          </div>

          <!-- Budget Amount -->
          <div class="mb-4">
            <div class="flex items-center justify-between text-sm text-gray-600 mb-1">
              <span>Spent</span>
              <span>Budget</span>
            </div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-2xl font-bold text-gray-900">
                {{ formatCurrency(budget.spent) }}
              </span>
              <span class="text-xl font-semibold text-gray-600">
                {{ formatCurrency(budget.amount) }}
              </span>
            </div>
          </div>

          <!-- Progress Bar -->
          <div class="mb-4">
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div
                class="h-3 rounded-full transition-all duration-300"
                :class="getProgressColor(budget.percentage)"
                :style="{ width: `${Math.min(budget.percentage, 100)}%` }"
              />
            </div>
            <div class="flex items-center justify-between mt-2 text-sm">
              <span :class="getTextColor(budget.percentage)">
                {{ budget.percentage.toFixed(1) }}% used
              </span>
              <span class="text-gray-600">
                {{ formatCurrency(budget.remaining) }} left
              </span>
            </div>
          </div>

          <!-- Status Badge -->
          <div v-if="budget.is_exceeded" class="bg-red-100 text-red-800 text-sm font-medium px-3 py-1 rounded-full inline-block">
            ⚠️ Budget Exceeded
          </div>
          <div v-else-if="budget.percentage >= 80" class="bg-yellow-100 text-yellow-800 text-sm font-medium px-3 py-1 rounded-full inline-block">
            ⚡ Almost there
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="budgets.length === 0" class="col-span-full text-center py-12">
          <p class="text-gray-500 mb-4">No budgets set for this month</p>
          <button @click="openAddModal" class="btn-primary">
            Create Your First Budget
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

