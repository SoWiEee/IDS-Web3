import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { md3 } from 'vuetify/blueprints'

const vuetify = createVuetify({
  blueprint: md3,
  theme: {
    defaultTheme: 'darkTheme',
    themes: {
      darkTheme: {
        dark: true,
        colors: {
          background: '#121212',
          surface: '#1E1E1E',
          primary: '#42b883',
          secondary: '#35495e',
        }
      }
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
})

export default vuetify