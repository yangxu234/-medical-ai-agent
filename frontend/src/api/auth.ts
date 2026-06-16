import api from './client'
import type { User, Token } from '@/types/user'

export const authApi = {
  async register(data: { email: string; name: string; password: string }): Promise<User> {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async login(email: string, password: string): Promise<Token> {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return response.data
  },

  async getMe(): Promise<User> {
    const response = await api.get('/auth/me')
    return response.data
  },
}
