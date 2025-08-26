import api from '../api'
import { Ref, ref } from 'vue'
import moment from 'moment/min/moment-with-locales'

type EventProgramItemDto = {
    id_program_item: string
    id_event: string
    id_location: string
    name: string
    description: string
    type: string
    attendee_limit: number
    attendee_limit_buffer: number
    required_time: number
    before_time_buffer: number
    after_time_buffer: number
    created_by: string
    created_at: string
    updated_by: string
    updated_at: string
}

export type EventProgramItemEntity = {
    id_program_item: string
    id_event: string
    id_location: string
    name: string
    description: string
    type: string
    attendee_limit: number
    attendee_limit_buffer: number
    required_time: number
    before_time_buffer: number
    after_time_buffer: number
    created_by: string
    created_at: moment.Moment
    updated_by: string
    updated_at: moment.Moment
}

const mapDtoToEntity = (dto: EventProgramItemDto): EventProgramItemEntity => {
    return {
        id_program_item: dto.id_program_item,
        id_event: dto.id_event,
        id_location: dto.id_location,
        name: dto.name,
        description: dto.description,
        type: dto.type,
        attendee_limit: dto.attendee_limit,
        attendee_limit_buffer: dto.attendee_limit_buffer,
        required_time: dto.required_time,
        before_time_buffer: dto.before_time_buffer,
        after_time_buffer: dto.after_time_buffer,
        created_by: dto.created_by,
        created_at: moment(dto.created_at),
        updated_by: dto.updated_by,
        updated_at: moment(dto.updated_at)
    }
}

export default function useProgramItem(): {
    programItems: Ref<Array<EventProgramItemEntity>>,
    fetchProgramItems: (id_event: string) => Promise<void>
} {
    const programItems = ref<Array<EventProgramItemEntity>>([])

    const fetchProgramItems = async (id_event: string) => {
        const response = await api.get(`event/${id_event}/programitem`)
        const data = await response.json<Array<EventProgramItemDto>>()
        programItems.value = data.map(mapDtoToEntity)
    }

    return {
        programItems,
        fetchProgramItems
    }
}