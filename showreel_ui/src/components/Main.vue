<template>
  <v-row>
    <v-container fluid>
      <v-card class="mx-auto" max-width="1200">
        <v-card-title>Clips</v-card-title>
          <v-data-iterator
            :items="clips"
            item-key="name"
            hide-default-footer
          >
            <template v-slot:default="{ items, isExpanded, expand }">
              <v-row>
                <v-col
                  v-for="item in items"
                  :key="item.index"
                  cols="12"
                  sm="6"
                  md="4"
                  lg="3"
                >
                  <v-card>
                    <v-card-title>
                      <h4>{{ item.name }}</h4>
                    </v-card-title>
                    <v-card-subtitle>
                      <h4>{{ `${item.standard}, ${item.definition}` }}</h4>
                    </v-card-subtitle>
                    <v-switch
                      :input-value="isExpanded(item)"
                      :label="isExpanded(item) ? 'Expanded' : 'Closed'"
                      class="pl-4 mt-0"
                      @change="(v) => expand(item, v)"
                    ></v-switch>
                    <v-divider></v-divider>
                    <v-list v-if="isExpanded(item)" dense>
                      <v-list-item>
                        <v-list-item-content>description:</v-list-item-content>
                        <v-list-item-content class="align-end">
                          {{ item.description }}
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>start_timecode:</v-list-item-content>
                        <v-list-item-content class="align-end">
                          {{ item.start_timecode }}
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>end_timecode:</v-list-item-content>
                        <v-list-item-content class="align-end">
                          {{ item.end_timecode }}
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                    <v-card-actions>
                      <v-btn icon v-on:click="add_clip(item)" :disabled="clipDisabled(item)">
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
            </template>
          </v-data-iterator>
        </v-card>
    </v-container>
    <v-container>
      <v-card class="mx-auto" max-width="1200">
        <v-card-title>Reel</v-card-title>
          <form>
            <v-text-field
              v-model="reel.name"
              label="Name"
              required
            ></v-text-field>
            <v-select
              v-model="reel.standard"
              :disabled="reel.standard!=''"
              :items="standards"
              label="Standard"
              required
            ></v-select>
            <v-select
              v-model="reel.definition"
              :disabled="reel.definition!=''"
              :items="definition"
              label="Defnition"
              required
            ></v-select>
          </form>
        <v-card-text>Duration: {{this.reel.duration}} </v-card-text>
        <v-card-actions>
          <v-btn
            text
            :disabled="reelDisabled()"
            @click="send_reel(true)"
          >
            Save Reel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-row>
</template>

<script>
import Axios from 'axios'
  export default {
    data: () => ({
      clips: [],
      standards: ["PAL", "NTSC"],
      definition: ["SD", "HD"],
      reel: {
        name: "",
        standard: "",
        definition: "",
        clips: [],
        duration: "",
      }
    }),
    methods: {
      async getClips() {
        try {
          let res = await Axios.get(
            "https://localhost:5000/clip"
          );
          console.log(res)
          this.clips = res.data;
          let index = 0;
          this.clips.forEach((item) => {
            item.index = index;
            index += 1
          })
        } catch (error) {
          console.log(error);
        }
      },
      async add_clip (item) {
        this.reel.clips.push(item)
        await this.send_reel(false)
      },
      async send_reel(save) {
        try {
          let clip_indexes = [];
          this.reel.clips.forEach((item)=> {
            clip_indexes.push(item.index)
          })
          let data = {
              name: this.reel.name,
              standard: this.reel.standard,
              definition: this.reel.definition,
              clips: clip_indexes,
              save: save
            };
            console.log(data)
          let res = await Axios.post("https://localhost:5000/reel/", data);
          this.reel.duration = res.data.duration;
        } catch (error) {
          console.log(error);
        }
      },
      clipDisabled(item) {
        let reel_ready = (this.reel.name == "" || this.reel.standard == "" || this.reel.definition == "");
        return reel_ready || item.standard != this.reel.standard || item.definition != this.reel.definition
      },
      reelDisabled() {
        let reel_ready = (this.reel.name == "" || this.reel.standard == "" || this.reel.definition == "" || this.reel.clips.length==0);
        return reel_ready
      },
    },
    created () {
      this.getClips();
    }
  }
</script>