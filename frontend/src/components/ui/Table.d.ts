export enum TableColumnType {
    TEXT = 'text',
    NUMBER = 'number',
    DATE = 'date',
    DELTATIME = 'deltatime'
}

export type TableColumn = {
    id: string
    title: string
    type?: TableColumnType
}
