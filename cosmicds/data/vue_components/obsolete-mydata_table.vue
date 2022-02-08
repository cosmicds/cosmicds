<template>
  <v-card>
    <v-card-title>
      My Galaxies
    </v-card-title>
    <v-data-table
      dense
      :headers="headers"
      :items="galaxies"
      :items-per-page="8"
      item-key="name"
      show-select
      hide-default-footer
      class="elevation-1"
    >
    </v-data-table>
  </v-card>
</template>

<script>
module.exports = {
  props: [],
  data: function () {
    return {
      selected: [],
      headers: [
        {
          text: "Galaxy Name",
          align: 'start',
          sortable: false,
          value: 'name'
        },
        { text: 'Galaxy Type', value: 'type' },
        { text: 'Velocity (km/s)', value: 'velocity' },
        { text: 'Distance (Mpc)', value: 'distance' },
      ],
      galaxies: [
        {
          name: "Haro 11",
          type: "irregular",
          velocity: 6421,
          distance: 62.3,
        },
        {
          name: "Hercules A",
          type: "elliptical",
          velocity: 10189,
          distance: 117.7,
        },
        {
          name: "GOODS North",
          type: "spiral",
          element: "H-alpha",
          velocity: 10034,
          distance: 138.1,
        },
        {
          name: "NGC 6052",
          type: "spiral",
          element: "H-alpha",
          velocity: 20219,
          distance: 125.6,
        },
        {
          name: "UGC 2369",
          type: "spiral",
          element: "H-alpha",
          velocity: 19963,
          distance: 208.79,
        },
      ],
    };
  },
};
</script>