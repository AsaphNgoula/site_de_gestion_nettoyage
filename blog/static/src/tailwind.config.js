/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/src/**/*.js',
    './**/templates/**/*.html', // Si vous avez d'autres dossiers templates
  ],
  theme: {
    extend: {
      colors: {
        'sage': '#9CAF88',
        'sage-dark': '#869776',
      },
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
}