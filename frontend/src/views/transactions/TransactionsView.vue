<script setup>
import { ref, onMounted, computed } from 'vue'
import { format } from 'date-fns'
import api from '@/services/api'
import Navbar from '@/components/layout/Navbar.vue'

const transactions = ref([])
const currentPage = ref(1)
const totalCount = ref(0)
const pageSize = 50

const filters = ref({
  type: '',
  date_from: '',
  date_to: '',
  search: '',
})

const showModal = ref(false)
const editingTransaction = ref(null)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

onMounted(() => {
  fetchTransactions()
})

const fetchTransactions = async () => {
  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      ...filters.value,
    })

    const response = await api.get(`/transactions/?${params}`)
    transactions.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to fetch transactions:', error)
  }
}

const applyFilters = () => {
  currentPage.value = 1
  fetchTransactions()
}

const clearFilters = () => {
  filters.value = {
    type: '',
    date_from: '',
    date_to: '',
    search: '',
  }
  applyFilters()
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchTransactions()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchTransactions()
  }
}

const openAddModal = () => {
  editingTransaction.value = null
  showModal.value = true
}

const editTransaction = (transaction) => {
  editingTransaction.value = transaction
  showModal.value = true
}

const deleteTransaction = async (id) => {
  if (!confirm('Are you sure you want to delete this transaction?')) return

  try {
    await api.delete(`/transactions/${id}/`)
    fetchTransactions()
  } catch (error) {
    console.error('Failed to delete transaction:', error)
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
    <Navbar />

    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Transactions</h1>
          <p class="mt-1 text-sm text-gray-500">Manage your income and expenses</p>
        </div>
        <button @click="openAddModal" class="btn-primary">
          + Add Transaction
        </button>
      </div>

      <!-- Filters -->
      <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <!-- Type Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select v-model="filters.type" class="input-field">
              <option value="">All</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>

          <!-- Date From -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">From Date</label>
            <input v-model="filters.date_from" type="date" class="input-field" />
          </div>

          <!-- Date To -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">To Date</label>
            <input v-model="filters.date_to" type="date" class="input-field" />
          </div>

          <!-- Search -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Search description..."
              class="input-field"
            />
          </div>
        </div>

        <div class="mt-4 flex justify-end space-x-2">
          <button @click="applyFilters" class="btn-primary">Apply Filters</button>
          <button @click="clearFilters" class="btn-secondary">Clear</button>
        </div>
      </div>

      <!-- Transactions List -->
      <div class="card">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="transaction in transactions" :key="transaction.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(transaction.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center space-x-2">
                    <span class="text-lg">{{ transaction.category_icon }}</span>
                    <span class="text-sm text-gray-900">{{ transaction.category_name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm text-gray-500">
                  {{ transaction.description || '-' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="transaction.type === 'income' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                  >
                    {{ transaction.type }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-medium"
                    :class="transaction.type === 'income' ? 'text-success-600' : 'text-danger-600'">
                  {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="editTransaction(transaction)" class="text-primary-600 hover:text-primary-900 mr-4">
                    Edit
                  </button>
                  <button @click="deleteTransaction(transaction.id)" class="text-red-600 hover:text-red-900">
                    Delete
                  </button>
                </td>
              </tr>

              <!-- Empty State -->
              <tr v-if="transactions.length === 0">
                <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                  No transactions found
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="px-6 py-4 flex items-center justify-between border-t">
          <div class="text-sm text-gray-700">
            Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, totalCount) }} of {{ totalCount }} results
          </div>
          <div class="flex space-x-2">
            <button
              @click="previousPage"
              :disabled="currentPage === 1"
              class="btn-secondary disabled:opacity-50"
            >
              Previous
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage === totalPages"
              class="btn-secondary disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Add/Edit Modal (Will be implemented) -->
    <!-- <TransactionModal v-if="showModal" @close="closeModal" /> -->
  </div>
</template>

