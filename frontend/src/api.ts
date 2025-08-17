import ky from 'ky'

export type ApiEventType = {
  id_event: string
  name: string
  description: string
  start_date: string
  end_date: string
  status: string
  created_at: string
  created_by: string | null
  updated_at: string | null
  updated_by: string | null
}

export type ApiListResponse<T> = {
  data: T[]
  limit: number
  offset: number
  total: number
}

const api = ky.create({
  prefixUrl: '/api',
  timeout: 5000
})

export default api
export { api }
