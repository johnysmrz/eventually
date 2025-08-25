<template>
    <span class="auto-form">
        <form @submit.prevent="handleSubmit" :id="formId">
            <span class="form-field" v-for="field in fields" :key="field.id">
                <label :for="`${formId}_${field.id}`">
                    {{ field.label }} <span class="form-field_required" v-if="field.required">*</span>
                </label>
                <FormInput :config="field" v-model="fieldValues[field.id]" :formId="formId" :forceValidation="forceValidation" />
            </span>
        </form>
        <span class="form-controls">
            <Button @click="handleCancel" class="btn-error">
                <i class="pi pi-times"></i>
                Zrušit
            </Button>
            <Button @click="handleSubmit" class="btn-primary" type="submit">
                <i class="pi pi-check"></i>
                Ok
            </Button>
        </span>
    </span>
</template>

<script setup lang="ts">
import { defineEmits } from 'vue'
import { ref, Ref } from 'vue'
import Button from './Button.vue'
import type { AutoFormConfig, AutoFormField } from './AutoForm'
import FormInput from './FormInput.vue'

const formId: string = crypto.randomUUID()

interface Props {
    config: AutoFormConfig | Promise<AutoFormConfig>
}

const props = defineProps<Props>()

const emit = defineEmits(['submit', 'cancel'])


const fields = ref<AutoFormField[]>([])
const fieldValues = ref<Record<string, any>>({})

let forceValidation = ref(false)

const handleSubmit = () => {
    const form = document.getElementById(formId) as HTMLFormElement | null
    if (form?.checkValidity()) {
        emit('submit', fieldValues.value)
    } else {
        forceValidation.value = true
    }
}

const handleCancel = () => {
    emit('cancel')
}

if (props.config instanceof Promise) {
    const cfg = await props.config
    fields.value = cfg.fields
}
</script>

<style lang="scss">
@use '../../config.scss' as config;
@use 'sass:color';

form {
    &>span.form-field {
        display: grid;
        grid-template-columns: 200px 1fr;
        grid-column-gap: 10px;
        grid-row-gap: 5px;
        margin-bottom: 10px;

        .form-field_required {
            color: config.$error-color;
        }

        .form-input {
            display: flex;
            flex-direction: column;
            width: 100%;

            &_errors {
                color: config.$error-color;
                padding: 0;
                margin: 2px 0px 0 5px;
                font-size: 80%;
                font-weight: bold;
                list-style-position: inside;
                list-style-type: square;
            }

            input {
                padding: 7px;
                border: 2px solid config.$surface-edge-color;
                color: config.$text-color;
                background-color: color.adjust(config.$surface-color, $lightness: 15%);
                border-radius: 4px;
                min-width: 250px;



                &[type="color"] {
                    padding: 0px;
                    height: 32px;
                    width: 100%;
                }
            }

            input.input-state {
                &__valid {
                    border-color: config.$success-color;
                }

                &__invalid {
                    border-color: config.$error-color;
                }
            }

        }

    }
}

span.form-controls {
    display: flex;
    margin-top: 20px;
    justify-content: space-evenly;

    button {
        padding-left: 30px;
        padding-right: 30px;
    }
}
</style>