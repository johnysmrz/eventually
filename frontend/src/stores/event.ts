import { defineStore } from 'pinia'
import api from '../api.ts'
import type { ApiEventType, ApiListResponse } from '../api.ts'
import moment from 'moment'


export type EventType = {
  id_event: string
  name: string
  description: string
  start_date: moment.Moment
  end_date: moment.Moment
  status: string
  created_at: moment.Moment
  created_by: string | null
  updated_at: moment.Moment | null
  updated_by: string | null
}

export const useEventStore = defineStore('event', {
  state: () => ({
    events: Array<EventType>(),
    error: null
  }),

  getters: {
    getById: (state) => (id: string): EventType | undefined => state.events.find(e => e.id_event === id),
    getAll: (state): Array<EventType> => state.events
  },

  actions: {
    async fetchAll() {
      try {
        const data = await api.get('event').json() as ApiListResponse<ApiEventType>
        for (const eventData of data.data) {
          const event: EventType = {
            id_event: eventData.id_event,
            name: eventData.name,
            description: eventData.description,
            start_date: moment(eventData.start_date),
            end_date: moment(eventData.end_date),
            status: eventData.status,
            created_at: moment(eventData.created_at),
            created_by: eventData.created_by,
            updated_at: eventData.updated_at ? moment(eventData.updated_at) : null,
            updated_by: eventData.updated_by
          }
          this.events.push(event)
        }
      } catch (err) {
        this.error = err
        throw err
      }
    }

  }
})
