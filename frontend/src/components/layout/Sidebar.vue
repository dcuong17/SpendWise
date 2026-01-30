<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import {
  HomeIcon,
  CreditCardIcon,
  WalletIcon,
  ChartBarIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()

const navItems = [
  { name: 'Dashboard', path: '/dashboard', icon: HomeIcon },
  { name: 'Transactions', path: '/transactions', icon: CreditCardIcon },
  { name: 'Budgets', path: '/budgets', icon: WalletIcon },
  { name: 'Analytics', path: '/analytics', icon: ChartBarIcon },
]

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const names = user.value.full_name?.split(' ') || ['User']
  return names.map(n => n[0]).join('').toUpperCase().slice(0, 2)
})
</script>


<template>
  <aside class="bg-white shadow-md h-screen sticky top-0 w-64">
    <div class="p-6">
      <!-- Logo -->
      <div class="flex items-center space-x-2 mb-8">
        <span class="text-3xl">💰</span>
        <span class="text-2xl font-bold text-primary-600">SpendWise</span>
      </div>

      <!-- Navigation -->
      <nav class="space-y-2">
        <router-link
          v-for="item in navItems"
          :key="item.name"
          :to="item.path"
          class="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600"
        >
          <component :is="item.icon" class="h-5 w-5" />
          <span class="font-medium">{{ item.name }}</span>
        </router-link>
      </nav>
    </div>

    <!-- User Section (Bottom) -->
    <div class="absolute bottom-0 left-0 right-0 p-6 border-t">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-medium">
          {{ userInitials }}
        </div>
        <div class="flex-1">
          <p class="text-sm font-medium text-gray-900">{{ user?.full_name }}</p>
          <p class="text-xs text-gray-500">{{ user?.email }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

