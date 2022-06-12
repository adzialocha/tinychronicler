import * as path from 'path';

import CopyPlugin from 'copy-webpack-plugin';

import type { Configuration } from 'webpack';

const DIR_DIST = 'static';
const DIR_SRC = 'src';

function getPath(...args: Array<string>): string {
  return path.join(__dirname, ...args);
}

const config: Configuration = {
  entry: getPath(DIR_SRC),
  output: {
    path: getPath(DIR_DIST),
    filename: 'index.js',
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
    alias: {
      '~': getPath(DIR_SRC),
    },
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        exclude: /node_modules/,
        loader: 'ts-loader',
      },
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: '**/*.{png,json,webm}',
          context: DIR_SRC,
          noErrorOnMissing: true,
        },
      ],
    }),
  ],
  devtool: 'source-map',
  stats: 'minimal',
};

export default config;
