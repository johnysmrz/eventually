import api from '../api.ts'
import { Ref, ref } from 'vue'
import moment from 'moment/min/moment-with-locales'
import type { AutoFormConfig } from '../components/ui/AutoForm.d.ts'


 type EventLocationDTO = {
    created_by: string | null
    created_at: string | null
    updated_by: string | null
    updated_at: string | null
    id_event: string
    id_location: string
    name: string
    lat?: number
    lon?: number
    color: string
}

export type EventLocationEntity = {
    created_by: string | null
    created_at: moment.Moment | null
    updated_by: string | null
    updated_at: moment.Moment | null
    id_event: string
    id_location: string
    name: string
    lat?: number
    lon?: number
    color: string
}

export type CreateEventLocationDTO = Omit<EventLocationDTO, 'id_event' | 'created_at' | 'updated_at' | 'created_by' | 'updated_by'>

const mapDtoToEntity = (dto: EventLocationDTO): EventLocationEntity => {
    return {
        created_by: dto.created_by,
        created_at: moment(dto.created_at),
        updated_by: dto.updated_by,
        updated_at: moment(dto.updated_at),
        id_event: dto.id_event,
        id_location: dto.id_location,
        name: dto.name,
        lat: dto.lat,
        lon: dto.lon,
        color: dto.color
    }
}

export default function useEventLocation(): {
    eventLocation: Ref<Array<EventLocationEntity>>,
    fetchEventLocation: (id_event: string) => Promise<void>,
    fetchEventAutoFormOptions: (id_event: string) => Promise<AutoFormConfig>,
    createEventLocation: (eventId: string, data: CreateEventLocationDTO) => Promise<void>,
    deleteEventLocation: (eventId: string, locationId: string) => Promise<void>,
    updateEventLocation: (eventId: string, locationId: string, data: CreateEventLocationDTO) => Promise<void>
} {
    const eventLocation = ref<Array<EventLocationEntity>>([])

    const fetchEventLocation = async (id_event: string) => {
        const response = await api.get(`event/${id_event}/location`)
        eventLocation.value = []
        const data = await response.json<Array<EventLocationDTO>>()
        for (const dto of data) {
            eventLocation.value.push(mapDtoToEntity(dto))
        }
    }

    const fetchEventAutoFormOptions = async (id_event: string) => {
        const response = await api.get(`event/${id_event}/location/$autoform`)
        return await response.json<AutoFormConfig>()
    }

    const createEventLocation = async (eventId: string, data: CreateEventLocationDTO) => {
        const response = await api.post(`event/${eventId}/location`, {json: data})
        const dto = await response.json<EventLocationDTO>()
        eventLocation.value.push(mapDtoToEntity(dto))
    }

    const deleteEventLocation = async (eventId: string, locationId: string) => {
        await api.delete(`event/${eventId}/location/${locationId}`)
        eventLocation.value = eventLocation.value.filter(location => location.id_event !== locationId)
    }

    const updateEventLocation = async (eventId: string, locationId: string, data: CreateEventLocationDTO) => {
        const response = await api.put(`event/${eventId}/location/${locationId}`, {json: data})
        const dto = await response.json<EventLocationDTO>()
        const index = eventLocation.value.findIndex(location => location.id_event === locationId)
        if (index !== -1) {
            eventLocation.value[index] = mapDtoToEntity(dto)
        }
    }

    return {
        eventLocation,
        fetchEventLocation,
        fetchEventAutoFormOptions,
        createEventLocation,
        deleteEventLocation,
        updateEventLocation
    }
}