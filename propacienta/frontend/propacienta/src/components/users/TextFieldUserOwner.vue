<template>
  <v-text-field
    color="cyan"
    :name="fieldname"
    :label="labelname"
    :type="type"
    v-model="content"
    @input="$emit('input', content)"
    :readonly="fieldReadonly"
    :clearable="!fieldReadonly"
    @click:append="toggleFieldReadonly"
    :append-icon="fieldReadonly ? 'mdi-pencil' : 'mdi-check'"
    :rules="rules"
    :suffix="suffix"
    ref="field"
  ></v-text-field>
</template>
<script>
export default {
  name: "TextFieldUserOwner",
  props: {
    fieldname: String,
    labelname: String,
    value: String,
    rules: Array || undefined,
    suffix: { type: String, default: "" },
    type: {
      type: String,
      default: "text",
    },
  },
  watch: {
    value: function (val) {
      this.content = val;
    },
  },
  data: function () {
    return {
      fieldReadonly: true,
      content: "",
    };
  },
  created: function () {
    this.content = this.value;
  },
  methods: {
    toggleFieldReadonly: function () {
      if (!this.fieldReadonly) {
        this.$emit("updated", {
          fieldname: this.fieldname,
          content: this.content,
        });
      }
      this.fieldReadonly = !this.fieldReadonly;
    },
  },
};
</script>
