<template>
  <v-card>
    <v-card-title>
      My Galaxies | Velocity Measurements
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
        { text: 'Line Element', value: 'element' },
        { text: 'Rest Wavelength (nm)', value: 'restwave' },
        { text: 'Measured Wavelength (nm)', value: 'measwave' },
        { text: 'Velocity (km/s)', value: 'velocity' },
        { text: 'Distance (Mpc)', value: 'distance' },
      ],
      galaxies: [
        {
          name: "Haro 11",
          type: "irregular",
          element: "H-alpha",
          restwave: 656.3,
          measwave: 669.7,
          velocity: "",
          distance: "",
        },
        {
          name: "Hercules A",
          type: "elliptical",
          element: "Ca or K",
          restwave: 123.4,
          measwave: 234.5,
          velocity: "",
          distance: 66,
        },
        {
          name: "GOODS North",
          type: "spiral",
          element: "H-alpha",
          restwave: 656.3,
          measwave: 725.6,
          velocity: "",
          distance: 277,
        },
        {
          name: "NGC 6052",
          type: "spiral",
          element: "H-alpha",
          restwave: 656.3,
          measwave: 666.6,
          velocity: "",
          distance: 139,
        },
        {
          name: "UGC 2369",
          type: "spiral",
          element: "H-alpha",
          restwave: 656.3,
          measwave: 676.8,
          velocity: "",
          distance: 187,
        },
        {
          name: "Abell 370",
          type: "irregular",
          element: "H-alpha",
          restwave: 656.3,
          measwave: 903.0,
          velocity: "",
          distance: 1648,
        },
      ],
    };
  },
};
</script>