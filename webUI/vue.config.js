const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false
})
module.exports = {
    pages: {
      index: {
        // entry for the pages
        entry: 'src/views/index/index.js',
        // the source template
        template: 'src/views/index/index.html',
        // output as dist/index.html
        filename: 'index.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'test',
        // chunks to include on this pages, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'index']
      },
      login: {
        // entry for the pages
        entry: 'src/views/login/login.js',
        // the source template
        template: 'src/views/login/login.html',
        // output as dist/index.html
        filename: 'login.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'Login',
        // chunks to include on this pages, by default includes
        // extracted common chunks and vendor chunks.
        chunks: ['chunk-vendors', 'chunk-common', 'index']
      }
    }
}