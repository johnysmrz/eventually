import api from '../api.ts'
import { Ref, ref } from 'vue'
import moment from 'moment/min/moment-with-locales'

type EventProgramOverviewDto = {
    id_program_item: string
    name: string
    type: string | null
    attendee_limit: number | null
    attendee_limit_buffer: number | null
    note: string | null
    status: string | null
    required_time: string | null
    before_time_buffer: string | null
    after_time_buffer: string | null
    start_time: string | null
    end_time: string | null
    attendee_count: number | null
}

export type EventProgramOverviewEntity = {
    id_program_item: string
    name: string
    type: string | null
    attendee_limit: number | null
    attendee_limit_buffer: number | null
    note: string | null
    status: string | null
    required_time: moment.Moment | null
    before_time_buffer: moment.Moment | null
    after_time_buffer: moment.Moment | null
    start_time: moment.Moment | null
    end_time: moment.Moment | null
    attendee_count: number | null
}

const mapDtoToEntity = (dto: EventProgramOverviewDto): EventProgramOverviewEntity => {
    return {
        id_program_item: dto.id_program_item,
        name: dto.name,
        type: dto.type,
        attendee_limit: dto.attendee_limit,
        attendee_limit_buffer: dto.attendee_limit_buffer,
        note: dto.note,
        status: dto.status,
        required_time: moment(dto.required_time),
        before_time_buffer: moment(dto.before_time_buffer),
        after_time_buffer: moment(dto.after_time_buffer),
        start_time: moment(dto.start_time),
        end_time: moment(dto.end_time),
        attendee_count: dto.attendee_count
    }
}

export default function useProgramOverview(): {
    programOverview: Ref<Array<EventProgramOverviewEntity>>,
    fetchProgramOverview: (id_event: string) => Promise<void>
} {
    const programOverview = ref<Array<EventProgramOverviewEntity>>([])

    const fetchProgramOverview = async (id_event: string) => {
        const response = await api.get(`event/${id_event}/program/overview`)
        const data = await response.json<Array<EventProgramOverviewDto>>()
        for (const dto of data) {
            programOverview.value.push(mapDtoToEntity(dto))
        }
    }

    return {
        programOverview,
        fetchProgramOverview
    }
}