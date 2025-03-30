const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: []
})

const path = require('path');
module.exports = defineConfig({
  transpileDependencies: [],
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    }
  }
});