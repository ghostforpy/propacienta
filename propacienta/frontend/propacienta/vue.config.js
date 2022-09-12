const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    https: true,
    allowedHosts: [
      'all'
    ],
  },
})
