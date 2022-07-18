<template>
  <b-field class="file is-warning" :class="{ 'has-name': !!file }">
    <b-upload
      v-model="file"
      class="file-label"
      rounded="true"
      @input="registerDestination"
    >
      <span class="file-cta">
        <b-icon class="file-icon" icon="upload" />
        <span class="file-label">{{ text }}</span>
      </span>
      <span v-if="file" class="file-name">
        {{ file.name }}
      </span>
    </b-upload>
  </b-field>
</template>

<script>
export default {
  name: "FolderSelector.vue",
  props: {
    text: String,
  },
  data() {
    return {
      file: null,
    };
  },

  methods: {
    registerDestination(input) {
      this.file = input;
      console.log(this.file);
    },
  },
};
</script>
