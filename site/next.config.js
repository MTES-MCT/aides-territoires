const withImages = require("next-images");
module.exports = withImages({
  webpack: (config, { defaultLoaders }) => {
    config.module.rules.push({
      test: /\.md?$/,
      use: [
        defaultLoaders.babel,
        {
          loader: "mdx-loader"
        }
      ]
    });
    return config;
  }
});
