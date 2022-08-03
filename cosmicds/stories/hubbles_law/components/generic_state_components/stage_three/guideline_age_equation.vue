<template>
  <scaffold-alert
    header-text="The Age of the Universe"
    @back="
      state.marker = 'ran_mar9';
    "
    @next="
      state.marker = 'ran_mar11';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Recall from our runners, that t = distance / velocity.
      </p>
      <p>
        To simplify the units astronomers use, we can write this as:
      </p>
      <p>
        Time (age of universe Gyr) = Distance in Mpc / velocity in km/s * :conversion factor to give time in Gyr:
      </p>
      <p>
        (A Gyr = 1 billion years).
      </p>
      <p>
        Use the distance and velocity of your “best fit galaxy” to calculate the age of the universe.
      </p>
      <p>
        Age measured with my dataset = _________ Gyr.
      </p>
    </div>
  </scaffold-alert>
</template>
