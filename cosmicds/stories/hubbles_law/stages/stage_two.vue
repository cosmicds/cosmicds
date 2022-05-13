<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <v-btn
          class="white-text px-a"
          color="success"
          @click="story_state.stage_index = 1"
        >Go back to Velocities</v-btn>
      </v-col>
    </v-row>

    <v-row class="d-flex align-stretch">
      <v-col cols="4">
        <c-distance-sidebar/>
      </v-col>
      <v-col cols="6">
        <v-card class="align-self-stretch">
          <c-distance-tool/>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <v-card
          class="pa-4"
          color="info"
          elevation="6"
        >
          Click a row to display the galaxy.
          <p>Click the ruler icon to activate the measuring tool and mark the edges of the galaxy.</p> 
          <p>Complete for all 5 galaxies</p>
        </v-card>        
      </v-col>
      <v-col cols="6">
        <jupyter-widget :widget="widgets.distance_table"/>      
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <v-card
          class="pa-4"
          color="info"
          elevation="6"
        >
          Click "Submit Age" to store result in database.
        </v-card>           
      </v-col>
      <v-col cols="4">
        <v-spacer></v-spacer>
      </v-col>
      <v-col cols="2" class="text-right">
        <v-btn
          class="white-text px-a"
          color="success"
          @click="submit_age()"
        >submit age</v-btn>
        <v-card 
          v-if="display_age"
          class="pa-2 mt-2"
          elevation="6"
          outlined 
        >
          Estimated age: {{ age_to_display }} Gy
        </v-card>
      </v-col>      
    </v-row>    
    <v-row>
      <v-col cols="4">
        <v-card
          class="pa-4"
          color="info"
          elevation="6"
        >
          Click "Start Over" to create entry for a new student.
        </v-card>           
      </v-col>
      <v-col cols="4">
        <v-spacer></v-spacer>
      </v-col>
      <v-col cols="2" class="text-right">
        <v-btn
          class="white-text px-a"
          color="success"
          @click="start_over()"
        >start over</v-btn>
      </v-col>      
    </v-row>   
    <v-row>
      <v-col cols="7">
        <v-spacer></v-spacer>
      </v-col>
      <v-col cols="3" class="text-right">
        <v-btn
          class="white-text px-a"
          color="accent"
          @click="story_state.stage_index = 3"
        >See Hubble Graph</v-btn>
      </v-col>      
    </v-row> 
  </v-container>
</template>
