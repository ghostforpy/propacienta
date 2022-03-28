<template>
  <v-expansion-panel>
    <v-expansion-panel-header>{{ computedStamp }}</v-expansion-panel-header>
    <v-expansion-panel-content class="break-word"
      >{{ cRes }}
      <v-list v-if="imgs.length > 0 || fils.length > 0" subheader two-line>
        <v-subheader inset v-if="imgs.length > 0">Изображения</v-subheader>
        <v-list-item
          v-for="(image, idx) in imgs"
          :key="image.delete_url"
          :href="image.image"
          :download="image.image.split('/').pop()"
        >
          <v-list-item-avatar>
            <v-icon class="grey lighten-1" dark> mdi-file-image </v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title
              v-text="image.image.split('/').pop()"
            ></v-list-item-title>
          </v-list-item-content>

          <v-list-item-action>
            <v-btn
              icon
              @click="deleteFileImg(idx, image.delete_url, $event, 'imgs')"
            >
              <v-icon color="red lighten-2">mdi-trash-can-outline</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
        <v-divider inset v-if="imgs.length > 0 && fils.length > 0"></v-divider>
        <v-subheader inset v-if="fils.length > 0">Файлы</v-subheader>
        <v-list-item
          v-for="(file, idc) in fils"
          :key="file.delete_url"
          :href="file.file"
          :download="file.file.split('/').pop()"
        >
          <v-list-item-avatar>
            <v-icon class="grey lighten-1" dark> mdi-file </v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title
              v-text="file.file.split('/').pop()"
            ></v-list-item-title>
          </v-list-item-content>

          <v-list-item-action>
            <v-btn
              icon
              @click="deleteFileImg(idc, file.delete_url, $event, 'files')"
            >
              <v-icon color="red lighten-2">mdi-trash-can-outline</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-list>
      <v-card-actions class="d-flex justify-end pm-0">
        <v-btn text color="red lighten-2" @click="$emit('delete', id)">
          Удалить
        </v-btn>
      </v-card-actions>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>
<script>
import request_service from "@/api/HTTP";
export default {
  name: "AnalisysResultCard",
  props: {
    id: Number,
    result: String,
    stamp: String,
    images: Array,
    files: Array,
  },
  data: function () {
    return {
      imgs: this.images,
      fils: this.files,
    };
  },
  computed: {
    cRes: function () {
      return this.result;
    },
    computedStamp: function () {
      let d = new Date(this.stamp);
      return d.toLocaleDateString();
    },
  },
  methods: {
    deleteFileImg: function (id, url, event, type) {
      event.preventDefault();
      var el = this;
      console.log(url);
      let config = {
        method: "delete",
        url: url,
      };
      request_service(
        config,
        function () {
          console.log("sucess");
          if (type == "files") {
            el.fils = el.fils.filter((item, idx) => {
              return idx != id;
            });
          } else {
            el.imgs = el.imgs.filter((item, idx) => {
              return idx != id;
            });
          }
        },
        function (error) {
          console.log(error);
        }
      );
    },
  },
};
</script>
<style>
.break-word {
  word-break: break-word;
}
</style>