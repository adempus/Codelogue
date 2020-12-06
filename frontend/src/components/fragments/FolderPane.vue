<template>
  <div id="folder_pane">
    <div class="p-grid p-fluid">
      <div class="p-col-12">
        <div id="new_folder_form" class="p-inputgroup">
          <InputText
            placeholder="New Folder"
            v-model="newFolderName"
            id="new_folder_name_input"
            :class="{ 'p-invalid': newFolderNameBlank }"
            aria-describedby="cannot_be_blank_error"
            v-on:keyup.enter="createNewFolder()"
          />
          <Button
            icon="pi pi-plus"
            class="p-button-warning"
            @click="createNewFolder()"
          />
        </div>
      </div>
      <small
        v-if="newFolderNameBlank"
        id="cannot_be_blank_error"
        class="p-invalid"
        >Folder name is required</small
      >
    </div>
  </div>
</template>

<script>
import { required, minLength } from "@vuelidate/validators";

export default {
  name: "FolderPane",
  data() {
    return {
      newFolderName: ""
    };
  },
  validations() {
    return {
      newFolderName: {
        required,
        minLength: minLength(3)
      }
    };
  },
  methods: {
    createNewFolder() {
      this.$v.$touch();
      if (this.$v.$error) {
        console.error("Folder name cannot be blank");
        return;
      }
      this.newFolderName = this.newFolderName.trim();
      console.log("new folder " + this.newFolderName + " created.");
      this.newFolderName = "";
      this.$v.$reset();
    }
  },
  computed: {
    newFolderNameBlank() {
      return this.$v.newFolderName.required.$invalid;
    }
  }
};
</script>

<style scoped>
#folder_pane {
  background-color: #272a36;
  height: 90vh !important;
  padding: 15px 15px 20px 15px;
}
#new_folder_form {
  padding-bottom: 15px;
}
#cannot_be_blank_error {
  position: relative;
  margin-top: -17px;
  padding-left: 10px;
}
#new_folder_name_input {
}
#new_folder_name_input:focus {
  outline: none;
  box-shadow: none;
}
</style>
