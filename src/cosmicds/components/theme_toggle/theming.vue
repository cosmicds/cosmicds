<template>
    <v-btn
        icon
        :disabled="disable"
        @click="countClicks"
        >
        <v-icon>
            {{ this.clicks === 1 ? this.on_icon : this.clicks === 2 ? this.off_icon : this.auto_icon }}
        </v-icon>
    </v-btn>
</template>
<script>
module.exports = {
    mounted() {
        if (window.solara) {
            if (localStorage.getItem(':solara:theme.variant')) {
                this.theme_dark = this.initTheme();
            } else {
                this.theme_dark = this.force_default || !this.enable_auto ? this.default_theme_bool() : null; 
            }
        }
        this.logThemeVariables('before clicks')
        // click values
        // 1 = dark, 2 = light, 3 = auto
        // theme_dark values
        // true = dark, false = light, null = auto
        if ( this.theme_dark === false ) {
            this.clicks = 2; 
        } else if ( this.theme_dark === null ) {
            this.clicks = 3;
        } else {
            this.clicks = 1;
        }
        
        this.lim = this.enable_auto ? 3 : 2;
        this.logThemeVariables('init');
    },
    methods: {
        logThemeVariables(where) {
            // debugging only
            const fmt = 'color: #0ff;font-size:16px;';
            // localStorage
            console.log(`%c[theming] [${where}] localStorage:solara:theme.variant: ${localStorage.getItem(':solara:theme.variant')}`, fmt);
            // theme.variant
            console.log(`%c[theming] [${where}] theme.variant: ${theme.variant}`, fmt);
            // theme_dark
            console.log(`%c[theming] [${where}] theme_dark: ${this.theme_dark}`, fmt);
            // default_theme
            console.log(`%c[theming] [${where}] default_theme: ${this.default_theme}`, fmt);
            // clicks
            console.log(`%c[theming] [${where}] clicks: ${this.clicks}`, fmt);
            // stringifyTheme
            console.log(`%c[theming] [${where}] stringifyTheme: ${this.stringifyTheme()}`, fmt);
            return;
        },
        to_theme_bool(theme_str) {
            // convert theme string to boolean
            // 'dark' => true, 'light' => false, 'auto' => null
            return theme_str === 'dark' ? true : theme_str === 'light' ? false : null;
        },
        to_theme_string(theme_bool) {
            // convert theme boolean to string
            // true => 'dark', false => 'light', null => 'auto'
            return theme_bool === true ? 'dark' : theme_bool === false ? 'light' : 'auto';
        },
        theme_to_clicks(theme_bool) {
            // convert theme boolean to clicks
            // true => 1, false => 2, null => 3
            return theme_bool === true ? 1 : theme_bool === false ? 2 : 3;
        },
        default_theme_bool() {
            if (!this.enable_auto && this.default_theme === 'auto' || this.default_theme === null) {
                return this.prefersDarkScheme();
            }
            return this.default_theme === 'dark' ? true : this.default_theme === 'light' ? false : null;
        },
        countClicks() {
            if ( this.clicks < this.lim ) {
                this.clicks++;
            } else {
                this.clicks = 1;
            }
            this.force_default = false;
            this.theme_dark = this.get_theme_bool( this.clicks );
        },
        get_theme_bool( clicks ) {
            if ( clicks === 3 ) {
                return null; // auto
            } else if ( clicks === 2 ) {
                return false; // light
            } else {
                return true; // dark
            }
        },
        stringifyTheme() {
            return this.to_theme_string(this.theme_dark)
        },
        initTheme() {
            storedTheme = JSON.parse(localStorage.getItem(':solara:theme.variant'));
            return storedTheme === 'dark' ? true : storedTheme === 'light' ? false : null;
        },
        setTheme() {
            if ( window.solara && this.theme_dark === null ) {
                this.$vuetify.theme.dark = this.prefersDarkScheme();
                return;
            }
            this.$vuetify.theme.dark = this.theme_dark;
        },
        prefersDarkScheme() {
            return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
        },
    },
    watch: {
        clicks: function (val) {
            if ( window.solara ) {theme.variant = this.stringifyTheme();}
            this.setTheme();
            if ( window.solara ) {localStorage.setItem(':solara:theme.variant', JSON.stringify(theme.variant));}
            this.sync_themes(this.theme_dark);
            this.logThemeVariables('watch:clicks');
        },
    }
}
</script>
