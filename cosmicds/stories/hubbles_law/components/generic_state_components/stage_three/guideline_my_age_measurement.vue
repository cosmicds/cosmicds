<template>
  <scaffold-alert
    header-text="The Age of the Universe"
    @back="
      state.marker = 'ran_mar10';
    "
    @next="
      state.marker = 'ran_mar12';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        Congratulations!!! You have made your very own measurement of the age of the universe!!!
      </p>
      <p>
        Now we need to think about how reliable your measurement is.
      </p>
    </div>
  </scaffold-alert>
</template>
