const { defineConfig } = require('@vue/cli-service')
const CompressionPlugin = require('compression-webpack-plugin')
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
        title: 'RAP',
        // chunks to include on this pages, by default includes
        // extracted common chunks and vendor chunks.
        //chunks: ['chunk-vendors', 'chunk-common', 'index']
      },
      home: {
        // entry for the pages
        entry: 'src/views/home/home.js',
        // the source template
        template: 'src/views/home/home.html',
        // output as dist/index.html
        filename: 'home.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Home',
      },
      search: {
        // entry for the pages
        entry: 'src/views/search/search.js',
        // the source template
        template: 'src/views/search/search.html',
        // output as dist/index.html
        filename: 'search.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Search',
      },
      reaction: {
        // entry for the pages
        entry: 'src/views/reaction/reaction.js',
        // the source template
        template: 'src/views/reaction/reaction.html',
        // output as dist/index.html
        filename: 'reaction.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Reactions',
      },
      addEnzyme: {
        // entry for the pages
        entry: 'src/views/addEnzyme/addEnzyme.js',
        // the source template
        template: 'src/views/addEnzyme/addEnzyme.html',
        // output as dist/index.html
        filename: 'addEnzyme.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Add Enzyme',
      },
      comment: {
        // entry for the pages
        entry: 'src/views/comment/comment.js',
        // the source template
        template: 'src/views/comment/comment.html',
        // output as dist/index.html
        filename: 'comment.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Comment',
      },
      buildReactions: {
        // entry for the pages
        entry: 'src/views/buildReactions/buildReactions.js',
        // the source template
        template: 'src/views/buildReactions/buildReactions.html',
        // output as dist/index.html
        filename: 'buildReactions.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Build Reactions',
      },
      RAPBuilder: {
        // entry for the pages
        entry: 'src/views/rapBuilder/rapBuilder.js',
        // the source template
        template: 'src/views/rapBuilder/rapBuilder.html',
        // output as dist/index.html
        filename: 'rapBuilder.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | RAP Builder',
      },
      PartHub2: {
        // entry for the pages
        entry: 'src/views/parthub2/parthub2.js',
        // the source template
        template: 'src/views/parthub2/parthub2.html',
        // output as dist/index.html
        filename: 'parthub2.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | PartHub 2',
      },
      parts: {
        // entry for the pages
        entry: 'src/views/parts/parts.js',
        // the source template
        template: 'src/views/parts/parts.html',
        // output as dist/index.html
        filename: 'parts.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | PartHub 2 Results',
      },
      treeMap: {
        // entry for the pages
        entry: 'src/views/treeMap/treeMap.js',
        // the source template
        template: 'src/views/treeMap/treeMap.html',
        // output as dist/index.html
        filename: 'treeMap.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Tree Map',
      },
      demo: {
        // entry for the pages
        entry: 'src/views/demo/demo.js',
        // the source template
        template: 'src/views/demo/demo.html',
        // output as dist/index.html
        filename: 'demo.html',
        // when using title option,
        // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        title: 'RAP | Demo',
      },
    },
  css:{
    loaderOptions:{
      less:{
        lessOptions: {
          javascriptEnabled: true,
          modifyVars: {
            'primary-color': '#e37654',
            'pagination-font-family': 'Barlow',
            'font-family': 'HarmonyOS_Sans, Helvetica, Arial, sans-serif'
          }
        }
      }
    }
  },
  chainWebpack: (config) => {
    config.plugin('compressionPlugin').use(new CompressionPlugin({
      test: /\.(js|css|less)$/,
      threshold: 1024,
      deleteOriginalAssets: false,
      minRatio: 0.3,
    }))
  },
}