/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",   // Django templates
    "./**/*.html",             // any other html in the project
    "./**/*.{js,jsx,ts,tsx}"   // if you have React/JS files
  ],
  theme: {
    extend: {},
  },
  plugins: [
    function ({ addComponents }) {
      addComponents({
        '.form-input': {
          '@apply mb-5 rounded-md border border-sky-200 bg-sky-100 px-5 py-2 text-sm placeholder:text-sky-300 placeholder:font-light focus:border-sky-500 focus:ring-2 focus:ring-sky-300 focus:outline-none': {},
        },
      })
    }
  ],
}
