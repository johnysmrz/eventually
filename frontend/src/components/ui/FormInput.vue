<template>
    <div class="form-input">
        <input
            :id="fieldId"
            :type="props.config.type"
            :placeholder="props.config.placeholder"
            :value="modelValue"
            :required="props.config.required"
            :pattern="props.config.pattern"
            :class="[`input-state__${status}`]"
            :min="props.config.min"
            :max="props.config.max"
            :step="props.config.step"
            @input="handleInput"
            @focus="handleFocus"
            @blur="handleRevalidate"
        />
        <ul class="form-input_errors" v-if="errors.length > 0">
            <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, h } from 'vue'
import type { AutoFormField } from './AutoForm.d.ts'
import { ref, Ref, watch } from 'vue'

const props = defineProps({
    config: {
        type: Object as () => AutoFormField,
        required: true
    },
    modelValue: {
        type: String as () => string,
        required: false,
    },
    formId: {
        type: String as () => string,
        default: 'form'
    },
    forceValidation: {
        type: Boolean,
        default: false
    }
})

const fieldId: string = `${props.formId}_${props.config.id}`
const errors: Ref<string[]> = ref([])
let status: Ref<string | null> = ref('pristine')

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const handleInput = (e: Event) => {
    const target = e.target as HTMLInputElement
    emit('update:modelValue', target.value)
}
const handleFocus = (e: Event) => {
    emit('focus', e)
}

watch(
    () => props.forceValidation,
    (newVal) => {
        if (newVal) {
            handleRevalidate()
        }
    }
)

if (props.config.type === 'color' && !props.modelValue) {
    emit('update:modelValue', '#4169E1')
}

const handleRevalidate = () => {
    const field = document.getElementById(fieldId) as HTMLInputElement | null
    if (field) {
        const isValid = field.checkValidity()
        errors.value = []
        if (!isValid) {
            status.value = 'invalid'
            if (field.validity.badInput) {
                errors.value.push('Špatný vstup')
            }
            if (field.validity.customError) {
                errors.value.push(field.validationMessage)
            }
            if (field.validity.patternMismatch) {
                errors.value.push('Vstup neodpovídá požadovanému vzoru.')
            }
            if (field.validity.rangeOverflow) {
                errors.value.push('Hodnota je příliš vysoká.')
            }
            if (field.validity.rangeUnderflow) {
                errors.value.push('Hodnota je příliš nízká.')
            }
            if (field.validity.stepMismatch) {
                errors.value.push('Hodnota není platný krok.')
            }
            if (field.validity.tooLong) {
                errors.value.push('Vstup je příliš dlouhý.')
            }
            if (field.validity.tooShort) {
                errors.value.push('Vstup je příliš krátký.')
            }
            if (field.validity.typeMismatch) {
                errors.value.push('Vstup není správného typu.')
            }
            if (field.validity.valueMissing) {
                errors.value.push('Toto pole je povinné.')
            }
        } else {
            status.value = 'valid'
        }
    }
}
</script>

<style scoped>


</style>