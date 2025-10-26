/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // Disallow production builds if there are type errors
    ignoreBuildErrors: false,
  },
  eslint: {
    // Disallow production builds if there are ESLint errors
    ignoreDuringBuilds: false,
  },
}

module.exports = nextConfig
