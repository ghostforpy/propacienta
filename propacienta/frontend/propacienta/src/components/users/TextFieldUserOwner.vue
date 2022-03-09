<template>
  <v-text-field
    color="cyan"
    :name="fieldname"
    :label="labelname"
    type="text"
    v-model="content"
    @input="$emit('input', content)"
    :readonly="fieldReadonly"
    :clearable="!fieldReadonly"
    @click:append="toggleFieldReadonly"
    :append-icon="fieldReadonly ? 'mdi-pencil' : 'mdi-check'"
    :rules="rules"
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
