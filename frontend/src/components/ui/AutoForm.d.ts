export type AutoFormConfig = {
    fields: AutoFormField[]
    groups: String[]
}

export type AutoFormFieldOptions = {
    [key: string]: string
}

export type AutoFormField = {
    id: string
    label: string
    type: string
    required: boolean
    pattern?: string
    options?: AutoFormFieldOptions[]
    group?: string | undefined
    step?: string
    min?: string
    max?: string
    placeholder?: string
}
