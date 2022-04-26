<template>
  <scaffold-alert
    header-text="Velocity Calculation"
    @back="
      state.marker = 'dop_cal1';
    "
    @next="
      state.marker = 'dop_cal3';
    "
  >
    <div
      class="mb-4"
    >
      <p>
        The Dopper equation looks like this:
      </p>
      <p>
        $$ v=c \left(\frac{\lambda_{\text{obs}}}{\lambda_{\text{rest}}}-1\right) $$
      </p>
      <p>
        where:
      </p>
      <p>      
        \(v\): velocity of your galaxy, in km/s <br>
        \(c\): speed of light, 300,000 km/s <br>
        \(\lambda_{\text{obs}}\): observed wavelength of spectral line in your galaxy <br>
        \(\lambda_{\text{rest}}\): rest wavelength of spectral line} <br>
      </p>
    </div>
  </scaffold-alert>
</template>
